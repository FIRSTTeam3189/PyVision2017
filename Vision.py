import cv2, numpy , VisionProcessor, VisionConfiguration, VisionTable, FrameGrabbers

config = VisionConfiguration.VisionConfiguration()

table = VisionTable.VisionTable('vision')

grabber = FrameGrabbers.MultithreadedFrameGrabber(0, config).start()
loops = 0
should_shutdown = False
table.send_is_online(True)

while not should_shutdown:
    # Process image read
    frame = grabber.current_frame
    boxes = VisionProcessor.process_image(frame, config)

    # Send how many images processed, and send how many boxes found
    table.send_loops(loops)
    table.send_boxes_found(len(boxes))
    loops += 1

    # See if we should shut down
    should_shutdown = table.get_should_shutdown()
    print loops
    
    for i in xrange(len(boxes)):
        table.send_box( boxes[i], i)


