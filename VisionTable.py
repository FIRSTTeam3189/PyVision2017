from networktables import NetworkTables

NetworkTables.initialize(server='10.31.89.2')
IS_ONLINE = 'is_online'
SHOULD_SHUTDOWN = 'should_shutdown'
TAKE_SNAPSHOT = 'should_snapshot'
LOOP_AMOUNT = 'loop_amount'

class VisionTable(object):
    def __init__(self, table_name):
        self.table = NetworkTables.getTable(table_name)

    def send_box(self, box, box_number):
        for i in xrange(len(box)):
            self.table.putNumber('box_%d_%d_x' % (box_number, i), box[i][0])
            self.table.putNumber('box_%d_%d_y' % (box_number, i), box[i][1])

    def send_is_online(self, is_online):
        self.table.putBoolean(IS_ONLINE, is_online)

    def get_should_shutdown(self):
        return self.table.getBoolean(SHOULD_SHUTDOWN, False)
    
    def get_should_snapshot(self):
        self.table.putBoolean(TAKE_SNAPSHOT, should_snapshot)
        
    def send_loops(self, loops):
        self.table.putNumber(LOOP_AMOUNT, loops)
