# Import OpenCV, numpy, VisionProcessor, VisionConfig, VisionTable

# Create VisionConfig (config = VisionConfig.VisionConfig())
# Create VisionTable (table = VisionTable.VisionTable('vision')

# Create Frame Grabber (grabber = cv2.VideoCapture(0))

# Enter While True
  # Read Frame (ret, frame = grabber.read())
  # Process frame (boxes = VisionProcessor.process_image(frame, config)
  
  # iterate through boxes
  # for i in xrange(len(boxes)):
    # Send each box (table.send_box(i, boxes[i]))
    
  # Thats it.
