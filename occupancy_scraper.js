"use strict";

const puppeteer = require("puppeteer");
const Promise = require("bluebird");
const {Storage} = require("@google-cloud/storage");

/** Google place IDs provided by
 * "https://developers.google.com/places/web-service/place-id".
 */
const ids = [
    {name:"Bioscience & Natural Resources Library", id:"ChIJ_____-B-hYARkH8qFkVlQZA"},
    {name:"Business School Library", id:"ChIJmY7BsDp8hYARfG23CBRdZdU"},
    {name:"Doe Memorial Library", id:"ChIJAQAAADl8hYARaxyuchGHTCw"},
    {name:"C. V. Starr East Asian Library", id:"ChIJAQCwhiZ8hYARhe-BsmCY4VI"},
    {name:"Kresge Engineering Library", id:"ChIJF4BsiyN8hYARLZ1vIPraljI"},
    {name:"Environmental Design Library", id:"ChIJLVUAUCV8hYARvXQnG_cbi4w"},
    {name:"Moffitt Library", id:"ChIJxWEsuCZ8hYAR48_Sst45khU"},
    {name:"Jean Gray Hargrove Music Library", id:"ChIJ__-_ciV8hYARxgPm1ycRiEQ"},
    {name:"Recreational Sports Facility", id:"ChIJ6xOXzCd8hYARJdVJ4oZ_ZRM"},
    {name:"Crossroads", id:"ChIJLyHpUS58hYAR-oxYbGr1Apg"},
    {name:"Hearst Gym Pool", id:"ChIJkaIwgCV8hYAREuqCJDO_BQc"},
    {name:"Spieker Aquatic Complex", id:"ChIJA-r4zCd8hYAR59QrukWWDhc"},
    {name:"Anthropology Library", id:"ChIJl2AF9C98hYARKec1ZTLyN7E"},
    {name:"The Bancroft Library", id:"ChIJoZpCSCV8hYARAEbWLD-SHhk"},
    {name:"Career Counseling Library", id:"ChIJATeQ7yd8hYARtIL0y4SiJIg"},
    {name:"Earth Sciences & Map Library", id:"ChIJlQ-QyDHsa4cRn5bWMGC7Qfc"},
    {name:"Ethnic Studies Library", id:"ChIJ7_YgsCV8hYARBreZ04Yc3N8"},
    {name:"Northern Regional Library Facility", id:"ChIJfaEr8F54hYARTaAjFURNejA"},
    {name:"Physics Astronomy Library", id:"ChIJQ4uQWSR8hYAREh0HC7_5oeY"},
    {name:"The Golden Bear Cafe", id:"ChIJHeudCiZ8hYARcYHT4f8yWsg"}
];

async function getHistogram(url, page) {
    /**
     * Given the url of a location, returns the occupancy data for
     * each day of the week.
     */
    await page.goto(url);
    await page.waitForSelector(".section-popular-times-graph");

    const popularTimesHistogram = await page.evaluate(() => {
        const graphs = {};
        const days = ["Su", "Mo", "Tu", "We", "Th", "Fr", "Sa"];
        let live = null;
        [...document.querySelectorAll(".section-popular-times-graph")]
            .forEach((graph, i) => {
                const day = days[i];
                graphs[day] = [];
                // Finds where x axis starts
                let graphStartFromHour;
                [...graph.querySelectorAll(".section-popular-times-label")]
                    .forEach((label, labelIndex) => {
                        if (graphStartFromHour) return;
                        const hourText = label.textContent.trim();
                        graphStartFromHour = hourText.includes("p") ? 12 + (parseInt(hourText) - labelIndex)
                                                : parseInt(hourText) - labelIndex;
                    });
                // Finds values from y axis
                [...graph.querySelectorAll(".section-popular-times-bar")]
                    .forEach((bar, barIndex) => {
                        const liveRegex = /(\d+)(\s+)?(%.+\s)(\d+)(\s+)?(%)/;
                        const usualRegex = /\d+(\s+)?%/;
                        const attr = bar.getAttribute("aria-label");
                        const occupancyMatch = attr.match(usualRegex);
                        const liveOccupancyMatch = attr.match(liveRegex);
                        const maybeHour = graphStartFromHour + barIndex;
                        const hour = maybeHour > 24 ? maybeHour - 24
                                        : maybeHour;
                        if (liveOccupancyMatch && liveOccupancyMatch.length) {
                            live = parseInt(liveOccupancyMatch[1]);
                            graphs[day].push({
                                hour: hour,
                                occupancyPercent: parseInt(liveOccupancyMatch[4])
                            });
                        } else if (occupancyMatch && occupancyMatch.length) {
                            graphs[day].push({
                                hour: hour,
                                occupancyPercent: parseInt(occupancyMatch[0])
                            });
                        }
                    });
            });
        graphs.live = live;
        return graphs;
    });
    return popularTimesHistogram;
}

async function getData() {
    /**
     * Returns data in the following schema:
     * location (string): {
        - live: occupancy %
        - day of week (string) : [array of {hour, occupancy %}]
        }    
     }
     */
    const browser = await puppeteer.launch({
        args: ["--no-sandbox"],
        headless: true
    });
    const page = await browser.newPage();

    // Catches console.log messages in page.evaluate() for debugging purposes
    page.on("console", function (msg) {
        for (let i = 0; i < msg.args().length; ++i)
            console.log(`${i}: ${msg.args()[i]}`);
    });

    const result = {};
    const URL_BASE = "https://www.google.com/maps/search/?api=1&query=Google&query_place_id=";
    for (let i = 0; i < ids.length; i++) {
        const url = URL_BASE + ids[i].id;
        try {
            const histogram = await getHistogram(url, page);
            if (histogram) {
                result[ids[i].name] = histogram;
            }
        } catch (e) {
            console.error(e);
        }
    }
    await page.close();
    await browser.close();
    return result;
}

exports.scrape = (req, res) => {
    getData().then((result) => {
        const storage = new Storage();
        const bucket = storage.bucket("bm-backend-scrap");
        const file = bucket.file("occupancy.json");
        const contents = JSON.stringify(result);
        file.save(contents, function(err) {
            if (err) {
                console.log(err);
            } else {
                res.status(200).send("Completed.");
            }
        });
    });
};
