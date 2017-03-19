from networktables import NetworkTables

NetworkTables.initialize(server='10.31.89.2')
IS_ONLINE = 'is_online'
SHOULD_SHUTDOWN = 'should_shutdown'
TAKE_SNAPSHOT = 'should_snapshot'
LOOP_AMOUNT = 'loop_amount'
BOXES_FOUND = 'boxes_found'
BOX_INFO_X = 'peg_x'
BOX_INFO_HAS = 'has_info'
BOX_INFO_INNER_LEFT = 'inner_left'
BOX_INFO_INNER_RIGHT = 'inner_right'
BOX_INFO_INNER_DISTANCE = 'inner_dist'
BOX_INFO_HEIGHT = 'height'
BOX_INFO_U = 'peg_u'

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

    def send_boxes_found(self, amount):
        self.table.putNumber(BOXES_FOUND, amount)

    def send_box_info(self, box_info):
        if box_info is None:
            self.table.putBoolean(BOX_INFO_HAS, False)
        else:
            self.table.putBoolean(BOX_INFO_HAS, True)
            self.table.putNumber(BOX_INFO_X, box_info.x)
            self.table.putNumber(BOX_INFO_INNER_LEFT, box_info.inner_left_x)
            self.table.putNumber(BOX_INFO_INNER_RIGHT, box_info.inner_right_x)
            self.table.putNumber(BOX_INFO_INNER_DISTANCE, box_info.inner_distance)
            self.table.putNumber(BOX_INFO_HEIGHT, box_info.box_height)
            self.table.putNumber(BOX_INFO_U, box_info.u)
            
