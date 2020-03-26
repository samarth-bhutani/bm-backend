"use strict";

const puppeteer = require("puppeteer");
const Promise = require("bluebird");
const {Storage} = require("@google-cloud/storage");

const locations = [
    "Bioscience & Natural Resources Library",
    "Business School Library",
    "Doe Memorial Library",
    "C. V. Starr East Asian Library",
    "Kresge Engineering Library",
    "Environmental Design Library",
    "Moffitt Library",
    "Jean Gray Hargrove Music Library",
    "Recreational Sports Facility"
];

/** Google place IDs provided by
 * "https://developers.google.com/places/web-service/place-id".
 */
const ids = [
    "ChIJ_____-B-hYARkH8qFkVlQZA",
    "ChIJmY7BsDp8hYARfG23CBRdZdU",
    "ChIJAQAAADl8hYARaxyuchGHTCw",
    "ChIJAQCwhiZ8hYARhe-BsmCY4VI",
    "ChIJF4BsiyN8hYARLZ1vIPraljI",
    "ChIJLVUAUCV8hYARvXQnG_cbi4w",
    "ChIJxWEsuCZ8hYAR48_Sst45khU",
    "ChIJ__-_ciV8hYARxgPm1ycRiEQ",
    "ChIJ6xOXzCd8hYARJdVJ4oZ_ZRM"
];

async function getHistogram(url, page) {
    /**
     * Given the url of a location, returns the occupancy data for
     * each day of the week.
     */
    await page.goto(url);
    await page.waitForSelector(".section-popular-times-graph");

    // Catches console.log messages in page.evaluate() for debugging purposes
    page.on("console", function (msg) {
        for (let i = 0; i < msg.args().length; ++i)
            console.log(`${i}: ${msg.args()[i]}`);
    });

    const popularTimesHistogram = await page.evaluate(() => {
        const graphs = {};
        const days = ["Su", "Mo", "Tu", "We", "Th", "Fr", "Sa"];
        let live = null;
        [...document.querySelectorAll(".section-popular-times-graph")]
            .forEach((graph, i) => {
                const day = days[i];
                graphs[day] = {};
                graphs[day].usual = [];
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
                            graphs[day].usual.push({
                                hour: hour,
                                occupancyPercent: parseInt(liveOccupancyMatch[4])
                            });
                        } else if (occupancyMatch && occupancyMatch.length) {
                            graphs[day].usual.push({
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
        - day of week (string) : {
            - live: {hour, occupancy %}
            - usual: array of {hour, occupancy %}
        }    
     }
     */
    try {
        const result = {};
        const URL_BASE = "https://www.google.com/maps/search/?api=1&query=Google&query_place_id=";
        const browser = await puppeteer.launch({
            args: ["--no-sandbox"],
            headless: true
        });
        const page = await browser.newPage();
        for (let i = 0; i < locations.length; i++) {
            const url = URL_BASE + ids[i];
            const histogram = await getHistogram(url, page);
            if (histogram) {
                result[locations[i]] = histogram;
            }
        }
        await page.close();
        await browser.close();
        return result;
    } catch (e) {
        console.error(e);
    }
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
