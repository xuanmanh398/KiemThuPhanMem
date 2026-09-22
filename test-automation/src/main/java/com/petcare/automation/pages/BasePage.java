package com.petcare.automation.pages;

import com.petcare.automation.utils.WaitUtils;
import org.openqa.selenium.*;
import org.openqa.selenium.interactions.Actions;
import org.openqa.selenium.support.ui.Select;

import java.util.List;

public abstract class BasePage {

    protected WebDriver driver;
    protected Actions actions;
    protected static final boolean VISUAL_DEMO_MODE = true; // Bật chế độ hiển thị viền đỏ và độ trễ để quan sát trực quan

    public BasePage(WebDriver driver) {
        this.driver = driver;
        this.actions = new Actions(driver);
    }

    /**
     * Làm nổi bật phần tử trên trang bằng viền đỏ và nền vàng trước khi thao tác
     */
    protected void highlightElement(WebElement element) {
        if (!VISUAL_DEMO_MODE) return;
        try {
            JavascriptExecutor js = (JavascriptExecutor) driver;
            js.executeScript("arguments[0].style.outline='3px solid #ef4444'; arguments[0].style.outlineOffset='2px';", element);
            sleep(250);
        } catch (Exception ignored) {}
    }

    protected void unhighlightElement(WebElement element) {
        if (!VISUAL_DEMO_MODE) return;
        try {
            JavascriptExecutor js = (JavascriptExecutor) driver;
            js.executeScript("arguments[0].style.outline=''; arguments[0].style.outlineOffset='';", element);
        } catch (Exception ignored) {}
    }

    protected void click(By locator) {
        try {
            WebElement element = WaitUtils.waitForClickable(driver, locator);
            scrollToElement(element);
            highlightElement(element);
            element.click();
            sleep(350);
        } catch (Exception e) {
            // Fallback sang Javascript click nếu bị header che khuất hoặc animation
            jsClick(locator);
        }
    }

    protected void jsClick(By locator) {
        WebElement element = WaitUtils.waitForPresence(driver, locator);
        scrollToElement(element);
        highlightElement(element);
        ((JavascriptExecutor) driver).executeScript("arguments[0].click();", element);
        sleep(350);
    }

    protected void sendKeys(By locator, String text) {
        WebElement element = WaitUtils.waitForVisibility(driver, locator);
        scrollToElement(element);
        highlightElement(element);
        element.clear();
        element.sendKeys(text);
        sleep(300);
    }

    protected String getText(By locator) {
        WebElement element = WaitUtils.waitForVisibility(driver, locator);
        highlightElement(element);
        String text = element.getText().trim();
        unhighlightElement(element);
        return text;
    }

    protected boolean isElementDisplayed(By locator) {
        try {
            WebElement element = WaitUtils.waitForVisibility(driver, locator);
            highlightElement(element);
            boolean displayed = element.isDisplayed();
            unhighlightElement(element);
            return displayed;
        } catch (Exception e) {
            return false;
        }
    }

    protected boolean isElementPresent(By locator) {
        try {
            return driver.findElements(locator).size() > 0;
        } catch (Exception e) {
            return false;
        }
    }

    protected void selectByVisibleText(By locator, String text) {
        WebElement element = WaitUtils.waitForVisibility(driver, locator);
        scrollToElement(element);
        highlightElement(element);
        Select select = new Select(element);
        select.selectByVisibleText(text);
        sleep(350);
    }

    protected void selectByValue(By locator, String value) {
        WebElement element = WaitUtils.waitForVisibility(driver, locator);
        scrollToElement(element);
        highlightElement(element);
        Select select = new Select(element);
        select.selectByValue(value);
        sleep(350);
    }

    protected void scrollToElement(WebElement element) {
        try {
            ((JavascriptExecutor) driver).executeScript("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", element);
            sleep(150);
        } catch (Exception ignored) {}
    }

    protected List<WebElement> findElements(By locator) {
        return driver.findElements(locator);
    }

    protected void sleep(long millis) {
        WaitUtils.sleep(millis);
    }
}
