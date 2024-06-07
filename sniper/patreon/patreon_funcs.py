from sniper.patreon import patreon_utils as utils

from sniper import scope

def filterFeed(driver, defaults=None):
    if defaults != None:
        type_default, tier_default, date_default, order_default = defaults
    else:
        type_default, tier_default, date_default, order_default = None, None, None, None
    
    type = "" if type_default == "0" else utils.handleFilter(driver, "Post type", "div.dAYgYF button.hjwRvq", "div.ekWcTy button", type_default)
    tier = "" if tier_default == "0" else utils.handleFilter(driver, "Tier", "div.dAYgYF button.hjwRvq", "a.iQxAKa", tier_default)
    if tier == "All posts":
        tier = "all"
    elif tier == "Posts you have access to":
        tier = "access"
    date = "" if date_default == "0" else utils.handleFilter(driver, "Date", "div.dAYgYF button.hjwRvq", "a.iQxAKa", date_default)

    order = "" if order_default == "0" else utils.toggleOrder(driver, order_default)
    return " ".join([item for item in [type, tier, date, order] if item != None]).strip()

def commandFeed(driver, defaults=None):
    utils.closeMembershipPopup(driver)
    utils.closeAppPopup(driver)
    filter_str = filterFeed(driver, defaults)
    # return [], filter_str
    # Process Posts while scrolling
    print("Processing Posts...")
    data_tuples = scope.whileScrolling(driver, utils.grabFeedPosts, sleep=2, expand=utils.grabExpandButtons)
    return data_tuples, filter_str