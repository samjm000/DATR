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

  // Deselect all checkboxes except for UK
  console.log("Deselecting all checkboxes except for UK...");
  await page.waitForSelector('input[data-country="uk"]', { timeout: 60000 });
  const checkboxes = await page.$$('input[type="checkbox"][data-country]');
  for (const checkbox of checkboxes) {
    const country = await page.evaluate(
      (el) => el.getAttribute("data-country"),
      checkbox
    );
    const isChecked = await page.evaluate((el) => el.checked, checkbox);
    if (country !== "uk" && isChecked) {
      try {
        await page.evaluate((el) => el.scrollIntoView(), checkbox);
        await page.evaluate((el) => el.click(), checkbox);
        console.log(`Deselected ${country}`);
      } catch (error) {
        console.error(`Error clicking checkbox for ${country}:`, error);
      }
    }
  }

  // Ensure the UK checkbox is checked
  const ukCheckbox = await page.$('input[data-country="uk"]');
  const ukChecked = await page.evaluate((el) => el.checked, ukCheckbox);
  if (!ukChecked) {
    await page.evaluate((el) => el.scrollIntoView(), ukCheckbox);
    await page.evaluate((el) => el.click(), ukCheckbox);
    console.log("Selected UK checkbox.");
  }

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

  // Extract horse details for each race
  for (const section of racecardSections) {
    for (const race of section.races) {
      console.log(`Navigating to ${race.link}`);
      await page.goto(race.link, { waitUntil: "networkidle2", timeout: 60000 });

      // Wait for the horse details to load
      console.log("Waiting for horse details to load...");
      await page.waitForSelector(".horse__details", { timeout: 60000 });

      // Extract horse details
      console.log("Extracting horse details...");
      const horseDetails = await page.evaluate(() => {
        const horses = [];
        const horseElements = document.querySelectorAll(
          ".horse__details a.horse__link"
        );
        horseElements.forEach((horseEl) => {
          const horseName = horseEl.innerText.trim();
          const horseLink = horseEl.href;
          horses.push({ name: horseName, link: horseLink });
        });
        return horses;
      });

      // Follow each horse link and get the Sire and Dam details
      for (const horse of horseDetails) {
        console.log(`Navigating to ${horse.link}`);
        await page.goto(horse.link, {
          waitUntil: "networkidle2",
          timeout: 60000,
        });

        // Wait for the Sire and Dam details to load
        console.log("Waiting for Sire and Dam details to load...");
        await page.waitForSelector(".column.width--tablet-12", {
          timeout: 60000,
        });

        // Extract Sire and Dam details
        console.log("Extracting Sire and Dam details...");
        const sireDamDetails = await page.evaluate(() => {
          const sire =
            document
              .querySelector(".column.width--tablet-12 ul li:nth-child(1)")
              ?.innerText.trim()
              .replace("Sire:", "")
              .trim() || "Sire not available";
          const dam =
            document
              .querySelector(".column.width--tablet-12 ul li:nth-child(2)")
              ?.innerText.trim()
              .replace("Dam:", "")
              .trim() || "Dam not available";
          const damsSire =
            document
              .querySelector(".column.width--tablet-12 ul li:nth-child(3)")
              ?.innerText.trim()
              .replace("Dam’s Sire:", "")
              .trim() || "Dam’s Sire not available";
          return { sire, dam, damsSire };
        });

        horse.sire = sireDamDetails.sire;
        horse.dam = sireDamDetails.dam;
        horse.damsSire = sireDamDetails.damsSire;
        console.log(`Extracted Sire and Dam details for ${horse.name}`);
      }

      race.horses = horseDetails;
      console.log(`Extracted ${horseDetails.length} horses from ${race.link}`);
    }
  }

  // Define the path to the JSON file
  const jsonFilePath = path.join(__dirname, "race_data.json");

  // Save the data to a JSON file
  fs.writeFileSync(jsonFilePath, JSON.stringify(racecardSections, null, 2));
  console.log("Race data saved to race_data.json");

  await browser.close();
  console.log("Puppeteer script completed.");
})();
