import numpy as np
import random
from tqdm import tqdm_notebook
import numba as nb

class VCG_Auction_Process(object):
    def __init__(self, value_mat_origin):
        self.value_mat_origin = value_mat_origin
        self.value_mat = self.value_mat_origin
        self.allocation = self.value_mat.columns  # For single-item condition
        self.best_price = 0  # Initialization

    @nb.jit
    def who_win(self):
        '''
        Pick up the winners for each item, if bids are the same, then a winner will be randomly picked
        '''
        self.winner_list = []  # Bidder index for each winner of the item
        self.second_price_list = []
        winner_temp = []
        for item_set in self.allocation:
            item_represent = item_set[0]  # Because all other items in the set share the same value
            winner_temp.append(np.where(self.value_mat[item_represent] == np.max(self.value_mat[item_represent]))[0])
        for item_set_index, winner in enumerate(winner_temp):
            item_set = self.allocation[item_set_index]  # The item set like [0,1]
            item_represent = item_set[0]  # Representation
            if len(winner) > 1:
                # print("Item set {:} has multiple winner: {:}".format(item_set,winner))
                random.seed(10)
                self.winner_list.append(random.choice(winner))
                second_price = sorted(self.value_mat[item_represent])[-2]
                # Add the payment of each winner, pay your value if the "same" occur
                self.second_price_list.append(second_price)
            else:
                self.winner_list.append(winner[0])
                second_price = sorted(self.value_mat[item_represent])[-2]
                self.second_price_list.append(second_price)
        # print(self.value_mat)
        # print(self.winner_list)
        return self.winner_list, self.second_price_list

    def winner_price(self):
        '''
        Calculate the price that the winner does to other agents and the mechanism will charge the price for each winner

        Make sure function who_win is run in advance
        '''
        self.welfare_list = []  # List for the welfare contributed by the winner. the sum of this list is the social welfare
        self.price_list = []  # List for the price that the winner charged, for losers they don't pay
        value_winner_list = []
        value_without_winner_list = []
        # Get the value list of winner
        # With the winners
        for item_set_index, winner in enumerate(self.winner_list):
            item_set = self.allocation[item_set_index]  # The item set like [0,1]
            item_represent = item_set[0]  # Representation
            value_winner_list.append(self.value_mat[item_represent].iloc[winner])
        self.welfare_list = value_winner_list
        # Without the winners
        value_without_winner_list = self.second_price_list
        # Contribution of the winner

        ctrib_list = list(map(lambda x: x[0] - x[1], zip(value_winner_list, value_without_winner_list)))
        # Price of the winner charged by the mechanism
        self.price_list = list(map(lambda x: x[0] - x[1], zip(value_winner_list, ctrib_list)))
        return self.price_list, self.welfare_list

    def allocate_items(self, allocation):
        '''
        Allocate different sets of items
        '''
        self.allocation = allocation  # Consider a finxed allocation case
        self.update_value_mat()

    @nb.jit
    def update_value_mat(self):
        '''
        Update the value of bidders for item sets as the value of item sets are the maximum value inside
        '''
        self.value_mat = self.value_mat_origin.copy()
        for set_index, item_set in enumerate(self.allocation):
            for bidder, value in self.value_mat.iterrows():
                self.value_mat.iloc[bidder][item_set] = np.max(self.value_mat.iloc[bidder][item_set])

    def find_best_allocation_price(self, current_price):
        if current_price >= self.best_price:
            self.best_allocation = self.allocation  # Initialization
            self.best_price = current_price

    def begin(self, possible_allocations):
        f = open('allocation_price.txt', 'w+')
        for allocation in tqdm_notebook(possible_allocations):  # Define your possible_allocations here:
            self.allocate_items(allocation)
            self.who_win()
            self.winner_price()
            self.find_best_allocation_price(np.sum(np.sum(self.price_list)))
            f.write('For Allocation: {:} Pirce charged by mechanism {:} and total {:}\n'.format(
                self.allocation, self.price_list, np.sum(self.price_list)))
        f.close()
        print('Best allocation: {:} and the mechanism charges {:}'.format(self.best_allocation, self.best_price))