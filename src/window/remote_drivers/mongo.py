"""
window.remote_drivers.mongo
~~~~~~~~~~~~~~~~

Class with auxiliary methods to store objects into MongoDB
"""
from pymongo import MongoClient


class MongoManager:
    """
    Class with auxiliary methods to store objects into MongoDB
    """

    @staticmethod
    def insert_alignment_object(alignment_dict):
        """
        It creates an alignment object that will serve as parent of the window alignments in
        a given communication.

        It will include the alignment configuration applied to all windows.
        :param alignment_dict: dict with the alignment object to store in Mongo
        :return: the ObjectID assigned to this alignment object
        """
        alignment_column = MongoManager._get_alignment_column()
        alignment_id = alignment_column.insert_one(alignment_dict)
        alignment_column.create_index('alignment_id')
        return alignment_id

    @staticmethod
    def insert_window_in_alignment(alignment_id, window_df):
        """
        It inserts a window alignment in MongoDB as a dictionary.
        :param alignment_id: The ObjectID of the parent alignment which contains the
        algorithm configuration
        :param window_df: the dataframe that contains the result of the window alignment
        """
        alignment_column = MongoManager._get_alignment_column()
        window_object = {
            'alignment_id': alignment_id,
            'window': window_df.to_dict('records')
        }
        alignment_column.insert_one(window_object)

    @staticmethod
    def _get_alignment_column():
        """
        This method returns the 'alignments' column in which all the alignment results are stored.

        You need to initialize a client in each subprocess to enable parallelization.
        """
        client = MongoClient()
        alignment_column = client['alignments-db']['alignments']
        return alignment_column
