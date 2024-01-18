from pymongo import MongoClient


class MongoManager:
    @staticmethod
    def insert_alignment_object(alignment_dict):
        alignment_column = MongoManager._get_alignment_column()
        alignment_id = alignment_column.insert_one(alignment_dict)
        alignment_column.create_index('alignment_id')
        return alignment_id

    @staticmethod
    def insert_window_in_alignment(alignment_id, window_df):
        alignment_column = MongoManager._get_alignment_column()
        window_object = {
            'alignment_id': alignment_id,
            'window': window_df.to_dict('records')
        }
        alignment_column.insert_one(window_object)

    @staticmethod
    def _get_alignment_column():
        """
        You need to initialize a client in each subprocess
        """
        client = MongoClient()
        alignment_column = client['alignments-db']['alignments']
        return alignment_column
