from sniper.patreon import patreon_utils as utils

from sniper import scope

def filterFeed(driver):
    type = utils.selectFilter(driver, "Post type", "div.ekWcTy button")
    tier = utils.selectFilter(driver, "Tier", "a.iQxAKa")
    if tier == "All posts":
        tier = "all"
    elif tier == "Posts you have access to":
        tier = "access"
    date = utils.selectFilter(driver, "Date", "a.iQxAKa")
    order = utils.toggleOrder(driver)
    return " ".join([item for item in [type, tier, date, order] if item != None]).strip()

def commandFeed(driver):
    utils.closeMembershipPopup(driver)
    utils.closeAppPopup(driver)
    filter_str = filterFeed(driver)
    # Process Posts while scrolling
    print("Processing Posts...")
    data_tuples = scope.whileScrolling(driver, utils.grabFeedPosts, sleep=2, expand=utils.grabExpandButtons)
    return data_tuples, filter_str