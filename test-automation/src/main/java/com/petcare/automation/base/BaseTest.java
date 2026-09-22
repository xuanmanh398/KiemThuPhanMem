package com.petcare.automation.base;

import com.petcare.automation.config.FrameworkConstants;
import com.petcare.automation.utils.ExtentReportListener;
import org.openqa.selenium.WebDriver;
import org.testng.annotations.AfterClass;
import org.testng.annotations.BeforeClass;
import org.testng.annotations.Optional;
import org.testng.annotations.Parameters;

public abstract class BaseTest {

    protected WebDriver driver;

    @BeforeClass(alwaysRun = true)
    @Parameters({"browser", "headless"})
    public void setUpClass(
            @Optional("") String browser,
            @Optional("false") String headless
    ) {
        String chosenBrowser = (browser != null && !browser.isEmpty()) ? browser : FrameworkConstants.DEFAULT_BROWSER;
        boolean isHeadless = Boolean.parseBoolean(headless) || FrameworkConstants.HEADLESS;

        driver = DriverFactory.initDriver(chosenBrowser, isHeadless);
        try {
            driver.manage().window().maximize();
        } catch (Exception ignored) {}
        driver.get(FrameworkConstants.APP_URL);
    }

    @AfterClass(alwaysRun = true)
    public void tearDownClass() {
        try {
            Thread.sleep(1000); // Giữ cửa sổ 1 giây để người xem quan sát kết quả trước khi đóng class
        } catch (InterruptedException ignored) {}
        DriverFactory.quitDriver();
    }

    public WebDriver getDriver() {
        return driver;
    }

    public void log(String stepMessage) {
        ExtentReportListener.logStep(stepMessage);
        System.out.println("[STEP] " + stepMessage);
    }
}
