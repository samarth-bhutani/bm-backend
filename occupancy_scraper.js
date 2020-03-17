const puppeteer = require('puppeteer');

(async () => {
    const browser = await puppeteer.launch();
    const page = await browser.newPage();
    const MOFFITT_URL = "https://www.google.com/maps/place/Moffitt+Library/@37.872574,-122.260748,15z/data=!4m5!3m4!1s0x0:0x159239deb2d2cfe3!8m2!3d37.872574!4d-122.260748"
    await page.goto(MOFFITT_URL);
    await page.waitForSelector('.section-popular-times-graph');
    let popularTimesHistogram = await page.evaluate(() => {
        const graphs = {};
        const days = ['Su', 'Mo', 'Tu', 'We', 'Th', 'Fr', 'Sa'];
        [...document.querySelectorAll('.section-popular-times-graph')].forEach((graph, i) => {
            const day = days[i];
            graphs[day] = [];
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
                const occupancyMatch = bar.getAttribute('aria-label').match(/\d+(\s+)?%/);
                if (occupancyMatch && occupancyMatch.length) {
                    const maybeHour = graphStartFromHour + barIndex;
                    graphs[day].push({
                        hour: maybeHour > 24 ? maybeHour - 24 : maybeHour,
                        occupancyPercent: parseInt(occupancyMatch[0]),
                    });
                }
            });
        });
        return graphs;
    });
    console.log(popularTimesHistogram);
    await browser.close();
})().catch( e => { console.error(e) } );