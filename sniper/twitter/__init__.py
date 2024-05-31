from sniper.twitter import twitter_funcs as funcs
from sniper.twitter import twitter_utils as utils

from sniper import scope, dir

def main(driver, command):
    targets = scope.readLines(dir.target)
    print(f"Sniper Engaged: {len(targets)} Targets Aquired")
    data_tuples = []
# Begin Iteration
    for target in targets:
        user = target
        scope.printProgress(targets, target)
        # Open URL
        scope.driverGet(driver, target, sleep=5)
# Command Types
        if command in ['media']:
            scope.driverGet(driver, f"https://twitter.com/{user}/media", sleep=5)
            data_tuples = funcs.commandMedia(driver)
            scope.write(f"{dir.root}\\{command} {user}.txt", data_tuples)