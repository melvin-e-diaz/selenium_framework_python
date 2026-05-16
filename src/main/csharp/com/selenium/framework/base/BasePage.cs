// BasePage.cs — C# port of BasePage.py (Selenium WebDriver).
// Add NuGet packages: Selenium.WebDriver, Selenium.Support (for WebDriverWait / SelectElement).

#nullable enable

using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Globalization;
using System.Linq;
using OpenQA.Selenium;
using OpenQA.Selenium.Interactions;
using OpenQA.Selenium.Support.UI;

namespace Com.Selenium.Framework.Base;

/// <summary>
/// Core helpers for Selenium UI automation, equivalent to the Python BasePage on PageFactory.
/// </summary>
public class BasePage
{
    public IWebElement? Element { get; set; }
    public IWebDriver Driver { get; }
    public WebDriverWait Wait { get; }
    public bool Highlight { get; set; }
    public bool MobileTest { get; set; }

    public BasePage(IWebDriver driver, int waitTimeoutSeconds = 10, bool highlight = true, bool mobileTest = false)
    {
        Driver = driver ?? throw new ArgumentNullException(nameof(driver));
        Wait = new WebDriverWait(driver, TimeSpan.FromSeconds(waitTimeoutSeconds));
        Highlight = highlight;
        MobileTest = mobileTest;
    }

    // -------------------------------------------------------------------------
    // Logging
    // -------------------------------------------------------------------------

    protected void Log(string message, string? description = null)
    {
        var timestamp = PrintTimestamp();
        if (!string.IsNullOrEmpty(description))
            Console.WriteLine($"{timestamp} | {message}: {description}");
        else
            Console.WriteLine($"{timestamp} | {message}");
    }

    /// <summary>Simple timestamped line (Python BasePage calls _log_simple from bp_scroll; not defined in BasePage.py).</summary>
    protected void LogSimple(string message)
    {
        Console.WriteLine($"{PrintTimestamp()} | {message}");
    }

    // -------------------------------------------------------------------------
    // Click
    // -------------------------------------------------------------------------

    public void BpClick(IWebElement element, string? description = null, string clickType = "left")
    {
        try
        {
            WaitUntilClickable(element);
            HighlightWebElement(element);
            switch (clickType.ToLowerInvariant())
            {
                case "left":
                    element.Click();
                    break;
                case "right":
                    new Actions(Driver).ContextClick(element).Perform();
                    break;
                case "double":
                    new Actions(Driver).DoubleClick(element).Perform();
                    break;
                default:
                    throw new ArgumentException($"Invalid click_type entered: {clickType}");
            }
            Log($"{clickType} clicked on element", description);
        }
        catch (Exception ex)
        {
            BpHandleError($"Failed to {clickType} click {description ?? "element"}: {ex.Message}");
            throw;
        }
    }

    public void BpClickAndHold(IWebElement element, string? description = null)
    {
        try
        {
            WaitUntilClickable(element);
            HighlightWebElement(element);
            new Actions(Driver).ClickAndHold(element).Perform();
            Log("Click and hold on element", description);
        }
        catch (Exception ex)
        {
            BpHandleError($"Failed to click and hold {description ?? "element"}: {ex.Message}");
            throw;
        }
    }

    public void BpReleaseClick(IWebElement element, string? description = null)
    {
        try
        {
            new Actions(Driver).Release(element).Perform();
            Log("Released click on element", description);
        }
        catch (Exception ex)
        {
            BpHandleError($"Failed to click and hold {description ?? "element"}: {ex.Message}");
            throw;
        }
    }

    public void BpMouseHover(IWebElement element, string? description = null, double? x = null, double? y = null)
    {
        try
        {
            HighlightWebElement(element);
            if (IsTruthy(x) && IsTruthy(y))
            {
                new Actions(Driver).MoveToElement(element, (int)x!.Value, (int)y!.Value).Perform();
            }
            else if (IsTruthy(x) || IsTruthy(y))
            {
                Log("WARNING: One offset coordinate is missing. Please check the code. Running hover method with no offset.", null);
                new Actions(Driver).MoveToElement(element).Perform();
            }
            else
            {
                new Actions(Driver).MoveToElement(element).Perform();
            }

            var message = IsTruthy(x) && IsTruthy(y)
                ? $"Mouse hover on element with offset ({x},{y})"
                : "Mouse hover on element";
            Log(message, description);
        }
        catch (Exception ex)
        {
            var errorMsg = IsTruthy(x) && IsTruthy(y)
                ? $"Failed to hover over {description ?? "element"} with offset ({x},{y})"
                : $"Failed to hover over {description ?? "element"} ";
            BpHandleError($"{errorMsg}: {ex.Message}");
        }
    }

    // -------------------------------------------------------------------------
    // Text
    // -------------------------------------------------------------------------

    public void BpWriteText(IWebElement element, string text, string? description = null, bool clearText = true)
    {
        try
        {
            WaitUntilVisible(element);
            HighlightWebElement(element);
            if (clearText)
                element.Clear();
            element.SendKeys(text);
            var desc = description ?? "unknown element";
            Log($"Wrote {text} to element {desc}");
        }
        catch (Exception ex)
        {
            BpHandleError($"Failed to write text to {description ?? "unknown element"}: {ex.Message}");
            throw;
        }
    }

    public string BpGetText(IWebElement element, string? description = null)
    {
        try
        {
            WaitUntilVisible(element);
            var text = element.Text;
            if (!string.IsNullOrEmpty(text))
                Log($"Returned text '{text}' from element.", description ?? "unknown element");
            else
                Log("WARNING: No text found in element.", description ?? "unknown element");
            return text;
        }
        catch (Exception ex)
        {
            BpHandleError($"Failed to get text from {description ?? "unknown element"}: {ex.Message}");
            throw;
        }
    }

    // -------------------------------------------------------------------------
    // Verification
    // -------------------------------------------------------------------------

    public bool BpIsChecked(IWebElement element, string? description = null)
    {
        try
        {
            WaitUntilVisible(element);
            var isChecked = element.Selected;
            Log($"Element checked status is {isChecked}", description ?? "unknown element");
            return isChecked;
        }
        catch (Exception ex)
        {
            BpHandleError($"Attempting to verify check/no check status failed for {description ?? "unknown element"}: {ex.Message}");
            return false;
        }
    }

    public bool BpIsDisplayed(IWebElement element, string? description = null)
    {
        try
        {
            WaitUntilVisible(element);
            var isDisplayed = element.Displayed;
            Log($"Element displayed is {isDisplayed}", description ?? "unknown element");
            return isDisplayed;
        }
        catch (Exception ex)
        {
            BpHandleError($"Attempting to verify displayed status failed for {description ?? "unknown element"}: {ex.Message}");
            throw;
        }
    }

    public bool BpIsEnabled(IWebElement element, string? description = null)
    {
        try
        {
            WaitUntilVisible(element);
            var isEnabled = element.Enabled;
            Log($"Element enabled is {isEnabled}", description ?? "unknown element");
            return isEnabled;
        }
        catch (Exception ex)
        {
            BpHandleError($"Attempting to verify enabled status failed for {description ?? "unknown element"}: {ex.Message}");
            throw;
        }
    }

    // -------------------------------------------------------------------------
    // Dropdown
    // -------------------------------------------------------------------------

    public void BpSelectFromDropdownList(IWebElement element, object textOrValue, string? description = null, bool selectByIndex = false)
    {
        try
        {
            WaitUntilVisible(element);
            var select = new SelectElement(element);
            if (selectByIndex)
            {
                var index = Convert.ToInt32(textOrValue, CultureInfo.InvariantCulture);
                select.SelectByIndex(index);
                Log($"Selected index {textOrValue} from element", description ?? "unknown element");
                return;
            }

            if (textOrValue is string s)
                select.SelectByText(s);
            else
                select.SelectByValue(Convert.ToString(textOrValue, CultureInfo.InvariantCulture));

            Log($"Selected option {textOrValue} from element", description ?? "unknown element");
        }
        catch (Exception ex)
        {
            BpHandleError($"Failed to select option {textOrValue} from dropdown list {description ?? "unknown element"}: {ex.Message}");
        }
    }

    public int BpGetNumItemsFromDropdownList(IWebElement element, string? description = null)
    {
        try
        {
            WaitUntilVisible(element);
            var select = new SelectElement(element);
            var numItems = select.Options.Count;
            Log($"Found {numItems} items in dropdown list.", description ?? "unknown element");
            return numItems;
        }
        catch (Exception ex)
        {
            BpHandleError($"Failed to return number of items in dropdown list {description ?? "element"}: {ex.Message}");
            throw;
        }
    }

    public IReadOnlyList<string> BpGetItemsFromDropdownList(IWebElement element, string? description = null, bool selectedItems = false)
    {
        try
        {
            WaitUntilVisible(element);
            var select = new SelectElement(element);
            IReadOnlyList<string> items = selectedItems
                ? select.AllSelectedOptions.Select(o => o.Text).ToList()
                : select.Options.Select(o => o.Text).ToList();

            if (items.Count == 0)
                Log("WARNING: No items found in dropdown list", description ?? "unknown list");
            else
            {
                Log($"{(selectedItems ? "Selected" : "All")} items found in dropdown list: ", description ?? "unknown list");
                foreach (var item in items)
                    Console.WriteLine($"    - {item}");
            }

            return items;
        }
        catch (Exception ex)
        {
            BpHandleError($"Failed to get items from {description ?? "element"}: {ex.Message}");
            throw;
        }
    }

    public bool BpVerifyItemPresentInDropdownList(IWebElement element, string item, string? description = null)
    {
        try
        {
            WaitUntilVisible(element);
            var select = new SelectElement(element);
            var isPresent = select.Options.Any(o => o.Text == item);
            Log($"{isPresent}: Item {item} is {(isPresent ? "present" : "not present")} in dropdown list", description ?? "unknown element");
            return isPresent;
        }
        catch (Exception ex)
        {
            BpHandleError($"Failed to verify presence of item {item} in dropdown list {description ?? "unknown element"}: {ex.Message}");
            throw;
        }
    }

    public void BpDeselectAllItemsFromDropdownList(IWebElement element, string? description = null)
    {
        try
        {
            WaitUntilVisible(element);
            var select = new SelectElement(element);
            select.DeselectAll();
            Log("All items deselected from dropdown list.", description ?? "unknown element");
        }
        catch (Exception ex)
        {
            BpHandleError($"Failed to deselect all items from {description ?? "unknown element"}: {ex.Message}");
            throw;
        }
    }

    // -------------------------------------------------------------------------
    // Move / scroll
    // -------------------------------------------------------------------------

    public void BpMoveToElement(IWebElement element, string? description = null)
    {
        try
        {
            new Actions(Driver).MoveToElement(element).Perform();
            Log("Moved to element", description ?? "unknown element");
        }
        catch (Exception ex)
        {
            BpHandleError($"Failed to move to {description ?? "unknown element"}: {ex.Message}");
            throw;
        }
    }

    public void BpScroll(string? direction = null, int? amount = null, int? x = null, int? y = null, IWebElement? element = null)
    {
        try
        {
            var js = (IJavaScriptExecutor)Driver;

            if (element is not null)
            {
                js.ExecuteScript("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", element);
                LogSimple($"Scrolled to element: {element}");
                return;
            }

            if (x is not null || y is not null)
            {
                var scrollX = x ?? 0;
                var scrollY = y ?? 0;
                js.ExecuteScript($"window.scrollTo({scrollX}, {scrollY});");
                Console.WriteLine($"{PrintTimestamp()} | Scrolled to coordinates: x={scrollX}, y={scrollY}");
                return;
            }

            if (direction is null)
                throw new ArgumentException("Must specify either direction, coordinates (x, y), or element");

            direction = direction.ToLowerInvariant();

            if (direction == "top")
            {
                js.ExecuteScript("window.scrollTo(0, 0);");
                LogSimple("Scrolled to top of page");
                return;
            }

            if (direction == "bottom")
            {
                js.ExecuteScript("window.scrollTo(0, document.body.scrollHeight);");
                LogSimple("Scrolled to bottom of page");
                return;
            }

            var scrollMap = new Dictionary<string, (int dx, int dy)>
            {
                ["down"] = (0, amount ?? 3000),
                ["up"] = (0, -(amount ?? 3000)),
                ["right"] = (amount ?? 1000, 0),
                ["left"] = (-(amount ?? 1000), 0)
            };

            if (!scrollMap.TryGetValue(direction, out var delta))
                throw new ArgumentException($"Invalid direction: {direction}. Must be one of: up, down, left, right, top, bottom");

            new Actions(Driver).ScrollByAmount(delta.dx, delta.dy).Perform();
            Console.WriteLine($"{PrintTimestamp()} | Scrolled {direction} by x={delta.dx}, y={delta.dy}");
        }
        catch (ArgumentException)
        {
            throw;
        }
        catch (Exception ex)
        {
            BpHandleError($"Failed to scroll: {ex.Message}");
            throw;
        }
    }

    public static DateTime BpReturnTodaysDate() => DateTime.Today;

    // -------------------------------------------------------------------------
    // Alerts / windows / browser
    // -------------------------------------------------------------------------

    public void BpHandleAlert(bool dismiss = false)
    {
        try
        {
            Wait.Until(d =>
            {
                try
                {
                    d.SwitchTo().Alert();
                    return true;
                }
                catch (NoAlertPresentException)
                {
                    return false;
                }
            });

            Log("Alert detected.");
            var alert = Driver.SwitchTo().Alert();
            Log("Alert text:", alert.Text);

            if (dismiss)
            {
                alert.Dismiss();
                Log("Alert dismissed.");
            }
            else
            {
                alert.Accept();
                Log("Alert accepted.");
            }
        }
        catch (Exception ex)
        {
            BpHandleError($"Failed to handle alert: {ex.Message}");
            throw;
        }
    }

    public void BpSwitchToNewWindow(int numWindowsOpen = 0)
    {
        try
        {
            var expected = numWindowsOpen + 2;
            Wait.Until(d => d.WindowHandles.Count >= expected);
            var handles = Driver.WindowHandles;
            Driver.SwitchTo().Window(handles[numWindowsOpen + 1]);
            Log($"Switched to new window: {numWindowsOpen + 1}");
        }
        catch (Exception ex)
        {
            BpHandleError($"Failed to switch to new window: {ex.Message}");
            throw;
        }
    }

    public void BpClosePopupWindow(int numWindowsToBeOpen = 1)
    {
        if (numWindowsToBeOpen < 1)
            throw new ArgumentException("ERROR: num_windows_to_be_open argument must be 1 or greater.");

        try
        {
            var windowsOpened = Driver.WindowHandles.ToList();
            BpBrowserClose();
            Driver.SwitchTo().Window(windowsOpened[numWindowsToBeOpen - 1]);
            Log("Closed popup window.");
        }
        catch (Exception ex)
        {
            BpHandleError($"Failed to close popup window: {ex.Message}");
            throw;
        }
    }

    public void BpBrowserBack()
    {
        try
        {
            Driver.Navigate().Back();
            Log("Browser back.");
        }
        catch (Exception ex)
        {
            BpHandleError($"Failed to navigate back in the browser: {ex.Message}");
            throw;
        }
    }

    public void BpBrowserForward()
    {
        try
        {
            Driver.Navigate().Forward();
            Log("Browser forward.");
        }
        catch (Exception ex)
        {
            BpHandleError($"Failed to navigate forward in the browser: {ex.Message}");
        }
    }

    public void BpBrowserRefresh()
    {
        try
        {
            Driver.Navigate().Refresh();
            Log("Browser refresh.");
        }
        catch (Exception ex)
        {
            BpHandleError($"Failed to refresh the browser: {ex.Message}");
        }
    }

    public void BpBrowserClose()
    {
        try
        {
            Driver.Close();
            Console.WriteLine($"{PrintTimestamp()} | Browser close");
        }
        catch (Exception ex)
        {
            BpHandleError($"Failed to close the browser window: {ex.Message}");
        }
    }

    /// <summary>Verifies column order matches sorting the cell texts in memory (string / numeric / date).</summary>
    public bool BpVerifyColumnSorting(IReadOnlyList<IWebElement> column, string? description = null, bool reverseSort = false, string sortType = "string", string dateFormat = "yyyy-MM-dd")
    {
        var originalList = column.Select(c => (c.Text ?? string.Empty).Trim()).ToList();
        var sortedList = originalList.ToList();

        try
        {
            if (string.Equals(sortType, "numeric", StringComparison.OrdinalIgnoreCase))
            {
                sortedList.Sort((a, b) => CompareNumericKeys(a, b, reverseSort));
            }
            else if (string.Equals(sortType, "date", StringComparison.OrdinalIgnoreCase))
            {
                sortedList.Sort((a, b) => CompareDateKeys(a, b, dateFormat, reverseSort));
            }
            else
            {
                sortedList.Sort((a, b) =>
                {
                    var cmp = string.Compare((a ?? "").ToLowerInvariant(), (b ?? "").ToLowerInvariant(), StringComparison.Ordinal);
                    return reverseSort ? -cmp : cmp;
                });
            }
        }
        catch (Exception ex)
        {
            BpHandleError($"Failed to sort column: {description ?? "unknown column"} | {ex.Message}");
            return false;
        }

        var isSorted = sortedList.SequenceEqual(originalList);
        var ascOrDesc = reverseSort ? "descending" : "ascending";

        if (isSorted)
        {
            Log($"TRUE: Column sorting verified in {ascOrDesc} order | Sort type: {sortType}", description ?? "unknown column");
            return true;
        }

        Log($"FALSE: Column sorting not verified in {ascOrDesc} order | Sort type: {sortType}", description ?? "unknown column");
        Console.WriteLine("=====ORIGINAL LIST=====");
        for (var i = 0; i < originalList.Count; i++)
            Console.WriteLine($"    {i + 1} | {originalList[i]}");
        Console.WriteLine("=====EXPECTED SORTED LIST=====");
        for (var i = 0; i < sortedList.Count; i++)
            Console.WriteLine($"    {i + 1} | {sortedList[i]}");
        return false;
    }

    public void BpSwitchToFrame(IWebElement iframe)
    {
        try
        {
            Wait.Until(d =>
            {
                try
                {
                    d.SwitchTo().Frame(iframe);
                    return true;
                }
                catch
                {
                    return false;
                }
            });
            Log($"Switched to frame {iframe}");
        }
        catch (Exception ex)
        {
            BpHandleError($"Failed to switch to iframe: {ex.Message}");
            throw;
        }
    }

    public void BpSwitchToDefaultContent()
    {
        try
        {
            Driver.SwitchTo().DefaultContent();
            Log("Switch to default content.");
        }
        catch (Exception ex)
        {
            BpHandleError($"Failed to switch to default content: {ex.Message}");
            throw;
        }
    }

    public string BpGetBrowserTitle
    {
        get
        {
            try
            {
                var title = Driver.Title;
                Log($"Browser title = {title}");
                return title;
            }
            catch (Exception ex)
            {
                BpHandleError($"Failed to get browser title: {ex.Message}");
                throw;
            }
        }
    }

    public void BpWaitForPageToLoad()
    {
        try
        {
            Log("Waiting for page to load.");
            var sw = Stopwatch.StartNew();
            Wait.Until(d => string.Equals(
                ((IJavaScriptExecutor)d).ExecuteScript("return document.readyState;")?.ToString(),
                "complete",
                StringComparison.Ordinal));
            sw.Stop();
            Log($"Time elapsed for page load: {sw.Elapsed.TotalSeconds:F2} seconds.");
        }
        catch (Exception ex)
        {
            BpHandleError($"Failed while waiting for page load: {ex.Message}");
        }
    }

    public static DateTime PrintTimestamp() => DateTime.Now;

    public static string BpGenerateRandomString(int stringLength)
    {
        const string chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789";
        var rnd = new Random();
        return new string(Enumerable.Range(0, stringLength).Select(_ => chars[rnd.Next(chars.Length)]).ToArray());
    }

    public bool BpVerifyUrl(string expectedUrl)
    {
        try
        {
            var actualUrl = Driver.Url;
            var isMatch = string.Equals(actualUrl, expectedUrl, StringComparison.Ordinal);
            if (isMatch)
                Log($"URL verified: {expectedUrl}");
            else
                Log($"URL NOT verified. Expected URL: {expectedUrl} | Actual URL: {actualUrl}");
            return isMatch;
        }
        catch (Exception ex)
        {
            BpHandleError($"Failed to verify URL: {ex.Message}");
            throw;
        }
    }

    public void BpHandleError(string errorText)
    {
        var timestamp = PrintTimestamp();
        Console.WriteLine($"{timestamp} | ERROR: {errorText}");
        Console.WriteLine(new StackTrace(true));
    }

    // -------------------------------------------------------------------------
    // Internals (PageFactory parity)
    // -------------------------------------------------------------------------

    protected void HighlightWebElement(IWebElement element)
    {
        if (!Highlight) return;
        ((IJavaScriptExecutor)Driver).ExecuteScript("arguments[0].style.border='2px ridge #33ffff'", element);
    }

    protected void WaitUntilClickable(IWebElement element)
    {
        Wait.Until(_ => element.Displayed && element.Enabled);
    }

    protected void WaitUntilVisible(IWebElement element)
    {
        Wait.Until(_ => element.Displayed);
    }

    private static bool IsTruthy(double? v) => v is { } n && Math.Abs(n) > double.Epsilon;

    private static int CompareNumericKeys(string? a, string? b, bool reverse)
    {
        var ka = NumericSortKey(a);
        var kb = NumericSortKey(b);
        var cmp = ka.CompareTo(kb);
        return reverse ? -cmp : cmp;
    }

    private static double NumericSortKey(string? x)
    {
        if (string.IsNullOrWhiteSpace(x)) return double.PositiveInfinity;
        return double.TryParse(x.Trim(), NumberStyles.Any, CultureInfo.InvariantCulture, out var n)
            ? n
            : double.PositiveInfinity;
    }

    private static int CompareDateKeys(string? a, string? b, string dateFormat, bool reverse)
    {
        var da = ParseDateOrMin(a, dateFormat);
        var db = ParseDateOrMin(b, dateFormat);
        var cmp = da.CompareTo(db);
        return reverse ? -cmp : cmp;
    }

    private static DateTime ParseDateOrMin(string? x, string dateFormat)
    {
        if (string.IsNullOrWhiteSpace(x)) return DateTime.MinValue;
        return DateTime.TryParseExact(x.Trim(), dateFormat, CultureInfo.InvariantCulture, DateTimeStyles.None, out var d)
            ? d
            : DateTime.MinValue;
    }
}
