# ===========================================================================================
# Base Producer
# Dev: anh.vu
# ===========================================================================================

"""
    Class này tạo ra producer dùng để gửi message lên topic trên kafka
"""

# ===========================================================================================
import json
import logging
import socket

import decouple
from confluent_kafka import Producer

# ===========================================================================================

# Sub Function ==============================================================================

def common_utils_acked(err, msg):
    if err is not None:
        logging.error("Failed to deliver message: %s: %s" % (str(msg), str(err)))
    else:
        logging.info("Message produced: %s" % (str(msg)))


# Main class ================================================================================

class BaseProducer(Producer):
    """
        Producer kafka custom
    """

    def __init__(self, server,
                 client_id=socket.gethostname()) -> None:

        super(BaseProducer, self).__init__(self._get_config(server=server,
                                                            client_id=client_id))

    def _get_config(self, server, client_id):
        config = {}

        if server is not None: config['bootstrap.servers'] = server
        if client_id is not None: config['client.id'] = client_id

        return config

    def send_message(self, topic, message, key=None, acked=common_utils_acked):
        if key is not None:
            self.produce(topic, value=message, key=key, callback=acked)
        else:
            self.produce(topic, value=message, callback=acked)
        self.poll(30)


class BaseLogProducer(Producer):
    """
        Producer kafka custom
    """

    def __init__(self, server,
                 client_id=socket.gethostname()) -> None:

        super(BaseLogProducer, self).__init__(self._get_config(server=server,
                                                            client_id=client_id))

    def _get_config(self, server, client_id):
        conf = {
            'bootstrap.servers': server
        }
        return conf

    def send_message(self, topic, message, key=None, acked=common_utils_acked):
        if key is not None:
            self.produce(topic, value=message, key=key, callback=acked)
        else:
            self.produce(topic, value=message, callback=acked)
        self.poll(0)

    def send_log(self, topic: str, message_object: dict):
        """
            Send message type log
        :param topic:
        :param message_object:
        :return:
        """
        try:
            message = json.dumps(message_object)
            self.produce(topic, value=message)
            self.poll(0)
        except Exception as e:
            logging.error(f'Send log message:[{message_object}] to Topic:[{topic}] error!-'
                          f'Caused: [{e.__str__()}]')
