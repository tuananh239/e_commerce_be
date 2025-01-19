# ===========================================================================================
# Fast API App
# Dev: anh.vu
# ===========================================================================================

"""
    * Class này được sử dụng để tạo ra một consumer subcribe một hoặc nhiều topic trên kafka
    để nhận tin nhắn mỗi khi có tin nhắn được gửi về topic đó trên kafka
"""

# ===========================================================================================

import ast
import json
from threading import Thread
from time import sleep

from confluent_kafka import Consumer, KafkaError

from app.libs.log.logger import logger

# ===========================================================================================

# Main class ================================================================================

class BaseComsumer(Thread):
    """
        Consumer được khởi tạo giống như một thread
    """

    def __init__(self, server, group_id) -> None:
        super(BaseComsumer, self).__init__()
        self._constructor(
            server=server,
            group_id=group_id
        )

    def _constructor(self, server, group_id) -> None:
        """
            Hàm khởi tạo:
                - is_app_running: Dùng để xác định ứng dụng có đang được chạy
                hay không, khi ứng dụng không được chạy thì đóng thread
                - topic: danh sách các topic mà comsumer đăng ký nhận tin nhắn
                trên kafka
                - consumer
        """
        self.is_app_running = True
        self.topic = []
        self.consumer = Consumer({
            'bootstrap.servers': server,
            'group.id': group_id,
            'auto.offset.reset': 'smallest',
            'partition.assignment.strategy': 'roundrobin'
        })

    def run(self):
        """
            Thực hiện chạy thread và bắt đầu kiểm tra tin nhắn có được gửi về
            topic đã subcribe hay không
        """
        try:
            self.consumer.subscribe(self.topic)
            while self.is_app_running:
                try:
                    message, success = self._scan_message(consumer=self.consumer, time_out=1.0)
                    if success:
                        self.handle_message(message=message)
                except Exception as e:
                    # push message to log
                    logger.error(msg=f"!!!!!! Handle message error: {e.__str__()}", send_kafka=False)
        except Exception as e:
            # push message to log
            logger.error(msg=f"!!!!!! Consumer has error: {e.__str__()}", send_kafka=False)
        finally:
            # Close down consumer to commit final offsets.
            logger.error(msg=f"!!!!!!  Consumer closed!!!!!", send_kafka=False)
            self.consumer.close()

    def handle_message(self, message):
        """
            Hàm xử lý message nhận được. Implement logic riêng cho từng yêu
            cầu đối với message nhận được trong class kế thừa
        """
        logger.info(msg=f'Receive message: {message}', send_kafka=False)

    def stop(self):
        """
            Unsubscribe consumer
        :return:
        """
        try:
            self.is_app_running = False
            self.consumer.unsubscribe()
            self.consumer.close()
        except RuntimeError:
            logger.error(msg=f'Unsubscribe topic failed - this consumer has closed.', send_kafka=False)
        except Exception as ker:
            logger.error(msg=f'Unsubscribe topic error -  caused by: {ker.__str__()}', send_kafka=False)
            

    def _scan_message(self, consumer, time_out):
        """
            Scan topics on kafka and receive message when have message on topic
            Input:
                consumer: Consumer is scanned
                time_out: time scan message on topics kafka
        """
        message = consumer.poll(timeout=time_out)

        if message is None:
            return None, False

        if message.error():
            if message.error().code() == KafkaError._PARTITION_EOF:
                # End of partition event
                logger.error(msg='%% %s [%d] reached end at offset %d\n' %
                              (message.topic(), message.partition(), message.offset()), send_kafka=False)
            else:
                logger.error(msg=message.error(), send_kafka=False)
                sleep(5)
            return None, False
        else:
            return self._deserialize_message(message), True
        

    def _deserialize_message(self, msg) -> str:
        """
            Convert message kafka to json data
        """
        try:
            return ast.literal_eval(msg.value().decode('utf8'))
        except ValueError:
            return json.loads(msg.value().decode('utf8'))
