const puppeteer = require('puppeteer');

(async () => {
    const browser = await puppeteer.launch();
    const page = await browser.newPage();
    const MOFFITT_URL = "https://www.google.com/maps/place/Moffitt+Library/@37.872574,-122.260748,15z/data=!4m5!3m4!1s0x0:0x159239deb2d2cfe3!8m2!3d37.872574!4d-122.260748"
    const RSF_URL = "https://www.google.com/maps/place/Recreational+Sports+Facility/@37.8685989,-122.262751,15z/data=!4m5!3m4!1s0x0:0x13657f86e249d525!8m2!3d37.8685989!4d-122.262751?hl=en"
    await page.goto(RSF_URL);
    await page.waitForSelector('.section-popular-times-graph');

    // Catches console.log messages in page.evaluate() for debugging purposes
    page.on('console', msg => {
        for (let i = 0; i < msg.args().length; ++i)
            console.log(`${i}: ${msg.args()[i]}`);
    });

    let popularTimesHistogram = await page.evaluate(() => {
        const graphs = {};
        const days = ['Su', 'Mo', 'Tu', 'We', 'Th', 'Fr', 'Sa'];
        [...document.querySelectorAll('.section-popular-times-graph')].forEach((graph, i) => {
            const day = days[i];
            graphs[day] = {};
            graphs[day]["live"] = null;
            graphs[day]["usual"] = [];
            // Finds where x axis starts
            let graphStartFromHour;
            [...graph.querySelectorAll('.section-popular-times-label')].forEach((label, labelIndex) => {
                if (graphStartFromHour) return;
                const hourText = label.textContent.trim();
                graphStartFromHour = hourText.includes('p')
                    ? 12 + (parseInt(hourText) - labelIndex)
                    : parseInt(hourText) - labelIndex;
            });
            // Finds values from y axis
            [...graph.querySelectorAll('.section-popular-times-bar')].forEach((bar, barIndex) => {
                const liveRegex = /(\d+)(\s+)?(%.+\s)(\d+)(\s+)?(%)/
                const usualRegex = /\d+(\s+)?%/
                const attr = bar.getAttribute('aria-label')
                const occupancyMatch = attr.match(usualRegex);
                const liveOccupancyMatch = attr.match(liveRegex);
                const maybeHour = graphStartFromHour + barIndex;
                const hour = maybeHour > 24 ? maybeHour - 24 : maybeHour;
                
                if (liveOccupancyMatch && liveOccupancyMatch.length) {
                    graphs[day]["live"] = {
                        hour: hour,
                        occupancyPercent: parseInt(liveOccupancyMatch[1])
                    };
                    graphs[day]["usual"].push({
                        hour: hour,
                        occupancyPercent: parseInt(liveOccupancyMatch[4])
                    })
                } else if (occupancyMatch && occupancyMatch.length) {
                    graphs[day]["usual"].push({
                        hour: hour,
                        occupancyPercent: parseInt(occupancyMatch[0])
                    });
                }
            });
        });
        return graphs;
    });
    console.log(JSON.stringify(popularTimesHistogram, null, 4));
    await browser.close();
})().catch( e => { console.error(e) } );