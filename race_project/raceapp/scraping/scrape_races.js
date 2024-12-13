const puppeteer = require("puppeteer");
const fs = require("fs");
const path = require("path");

(async () => {
  console.log("Starting Puppeteer script...");

  const browser = await puppeteer.launch({ headless: false });
  const page = await browser.newPage();
  await page.goto("https://www.attheraces.com/racecards/tomorrow", {
    waitUntil: "networkidle2",
    timeout: 60000,
  });

  // Wait for the cookie popup and click the 'Agree' button
  console.log("Waiting for the cookie popup...");
  await page.waitForSelector(".css-gz84ql", { timeout: 60000 });
  await new Promise((resolve) => setTimeout(resolve, 2000));
  await page.click(".css-gz84ql");
  console.log("Clicked 'Agree' button on the cookie popup.");

  // Wait for the fixture groups to load
  console.log("Waiting for the fixture groups to load...");
  await page.waitForSelector("#fixtures-grouped-by-meeting", {
    timeout: 60000,
  });

  // Get racecard sections
  console.log("Extracting racecard sections...");
  const racecardSections = await page.$$eval(
    "#fixtures-grouped-by-meeting .expandable.js-expandable",
    (sections) => {
      return sections.map((section) => {
        const racecardName = section.querySelector("h2")
          ? section.querySelector("h2").innerText.trim()
          : "Name not available";
        const races = [];
        const raceElements = section.querySelectorAll(
          '.meeting-list a[href^="/racecard/"]'
        );
        raceElements.forEach((raceEl) => {
          const raceLink = raceEl.href;
          const raceTitle = raceEl.querySelector("span.h7")
            ? raceEl.querySelector("span.h7").innerText.trim()
            : "Race title not available";
          const raceDetails = raceEl.querySelector("small")
            ? raceEl.querySelector("small").innerText.trim()
            : "Details not available";
          races.push({
            link: raceLink,
            title: raceTitle,
            details: raceDetails,
          });
        });
        return { racecardName, races };
      });
    }
  );

  console.log(`Extracted ${racecardSections.length} racecard sections.`);

  // Define the path to the JSON file
  const jsonFilePath = path.join(__dirname, "race_data.json");

  // Save the data to a JSON file
  fs.writeFileSync(jsonFilePath, JSON.stringify(racecardSections, null, 2));
  console.log("Race data saved to race_data.json");

  await browser.close();
  console.log("Puppeteer script completed.");
})();
