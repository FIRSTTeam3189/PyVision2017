import cv2, numpy , VisionProcessor, VisionConfiguration, VisionTable, FrameGrabbers
from BoxInfo import BoxInfo

config = VisionConfiguration.VisionConfiguration()

table = VisionTable.VisionTable('vision')

grabber = FrameGrabbers.MultithreadedFrameGrabber(0, config).start()
loops = 0
fails = 0
should_shutdown = False
table.send_is_online(True)

while not should_shutdown:
    # Process image read
    frame = grabber.current_frame
    if frame is None:
        fails += 1
        if fails > 200:
            print('Fail limit exceeded')
            exit(-1)
        continue
    boxes = VisionProcessor.process_image(frame, config)

    # Send how many images processed, and send how many boxes found
    table.send_loops(loops)
    table.send_boxes_found(len(boxes))
    loops += 1

    # See if we should shut down
    should_shutdown = table.get_should_shutdown()

    if loops % 100 == 0:
        print loops

    if config.show_image:
        frame = VisionProcessor.draw_box_info(frame, boxes)
        cv2.imshow('Original', frame)
        if cv2.waitKey(1) & 0xff == ord("q"):
            break
    
    for i in xrange(len(boxes)):
        table.send_box( boxes[i], i)

    if len(boxes) == 2:
        table.send_box_info(BoxInfo(boxes))
    else:
        table.send_box_info(None)
