import math
import requests
import sys
import json

TS_START = 1231006505

def get_timestamp_by_block_index(idx):
    response_curr_block = requests.get("https://blockchain.info/block-height/" + str(idx) + "?format=json")
    curr_block = json.loads(response_curr_block.text)
    ts_curr = curr_block["blocks"][0]["time"]
    return ts_curr

response_latestblock = requests.get("https://blockchain.info/latestblock")
latest_block = json.loads(response_latestblock.text)

def get_timestamp_of_latest_block():
    t_last_block = latest_block["time"]
    return t_last_block

def get_idx_of_latest_block():
    idx_last_block = latest_block["height"]
    return idx_last_block

def get_block_index(ts_input):
    latest_block_timstamp = get_timestamp_of_latest_block()
    latest_block_index = get_idx_of_latest_block()

    # check if the time is valid
    if ts_input > latest_block_timstamp or ts_input < TS_START:
        raise ValueError

    # for case ts_curr > ts_input
    ts_bigger_block_lower_than_input = TS_START
    idx_bigger_block_lower_than_input = 0
    # for case ts_curr < ts_input
    ts_lowest_block_bigger_than_input = latest_block_timstamp
    idx_lowest_block_bigger_than_input = latest_block_index

    # the number of blocks there are from the input time to the start time
    blocks_number = (ts_input-TS_START) / (60 * 10)
    blocks_number= math.floor(blocks_number)
    idx_curr = blocks_number
    ts_curr = get_timestamp_by_block_index(idx_curr)

    while blocks_number >= 1:
        if ts_curr > ts_input:
            # compute_average
            new_average = (ts_curr - ts_bigger_block_lower_than_input) / (60 * (
                        idx_curr - idx_bigger_block_lower_than_input))
            new_average = math.floor(new_average)
            # this is the number of blocks in the area between input to curr
            blocks_number = (ts_curr - ts_input) / (60 * new_average)
            # update the current index
            idx_curr = idx_curr - blocks_number
            idx_curr = math.floor(idx_curr)

        if ts_curr < ts_input:
            # compute_average
            new_average = (ts_lowest_block_bigger_than_input - ts_curr) / (60 * (
                        idx_lowest_block_bigger_than_input - idx_curr))
            new_average = math.ceil(new_average)
            # this is the number of blocks in the area between input to curr
            blocks_number = (ts_input - ts_curr) / (60 * new_average)
            # update the current index
            idx_curr = idx_curr + blocks_number
            idx_curr = math.ceil(idx_curr)

        ts_curr = get_timestamp_by_block_index(idx_curr)

    return idx_curr

ts_input = int(sys.argv[1])
Output = get_block_index(ts_input)
print(Output)
