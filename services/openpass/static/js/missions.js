const missions = [
    {
      name: "Test Mission",
      enabled: true,
      
      img: "img_avatar2.png",
      link:"runMission.py&p1=flyStream",
      
      description:"Quick Test! Start a video stream",
      tags:["test", "prebuilt", "stream"],
      
      long_description: 
      "Test our systems with a quick pre-built mission! \
      <br/><br/>The drone will start a video stream and record the next 10 seconds.",
    },
    {
      name: "Test Flight Mission",
      enabled: true,
      
      img: "img_avatar2.png",
      link:"runMission.py&p1=flyTest",
      
      description:"Quick Test! Takeoff and Land.",
      tags:["test", "prebuilt", "takeoff"],
      
      long_description: 
      "Test our systems with a quick pre-built mission! \
      <br/><br/>The drone will takeoff and land in the same spot \
      <br/><br/> Actions: \
      <br/>  1) Takeoff \
      <br/>  2) Land",
    },
    {
      name: "Forward Mission (1m)",
      enabled: true,
      
      img: "img_avatar2.png",
      link:"runMission.py&p1=flyForward&p2=1",
      
      description:"Takeoff, Fly 1m Forward, and Land",
      tags:["test", "prebuilt", "forward"],
      
      long_description:
      "Test our systems with a quick pre-built mission! \
      <br/><br/>The drone will takeoff, fly 1m forward, and land. \
      <br/><br/> Actions: \
      <br/>  1) Takeoff \
      <br/>  2) Fly 1m forward \
      <br/>  3) Land",
    },
    {
      name: "Forward Mission (5m)",
      enabled: true,
      
      img: "img_avatar2.png",
      link:"runMission.py&p1=flyForward&p2=5",
      
      description:"Takeoff, Fly 5m Forward, and Land",
      tags:["test", "prebuilt", "forward"],
      
      long_description:
      "Test our systems with a quick pre-built mission! \
      <br/><br/>The drone will takeoff, fly 5m forward, and land. \
      <br/><br/> Actions: \
      <br/>  1) Takeoff \
      <br/>  2) Fly 5m forward \
      <br/>  3) Land",
    },
    {
      name: "Square Mission (1m)",
      enabled: true,
      
      img: "img_avatar2.png",
      link:"runMission.py&p1=flySquare&p2=1",
      
      description:"Fly in a 1m square",
      tags:["test", "prebuilt", "square"], 
      
      long_description:
      "Test our systems with a quick pre-built mission! \
      <br/><br/>The drone will fly in a 1m square. \
      <br/><br/> Actions: \
      <br/>  1) Takeoff \
      <br/>  2) Fly in a 1m square \
      <br/>  3) Land \
      <br/><br/><b>** Starting at the bottom left corner **</b>",
    },
    {
      name: "Square Mission (5m)",
      enabled: true,
      
      img: "img_avatar2.png",
      link:"runMission.py&p1=flySquare&p2=5",
      
      description:"Fly in a 5m square",
      tags:["test", "prebuilt", "square"], 
      
      long_description:
      "Test our systems with a quick pre-built mission! \
      <br/><br/>The drone will fly in a 5m square. \
      <br/><br/> Actions: \
      <br/>  1) Takeoff \
      <br/>  2) Fly in a 5m square \
      <br/>  3) Land \
      <br/><br/><b>** Starting at the bottom left corner **</b>",
    },
    {
      name: "Lawnmower Mission (1m)",
      enabled: true,
      
      img: "img_avatar2.png",
      link:"runMission.py&p1=flyLawnmower&p2=1&p3=2",
      
      description:"Survey a 1m square",
      tags:["test", "prebuilt", "lawnmower"],
      
      long_description:
      "Test our systems with a quick pre-built mission! \
      <br/><br/>The drone will survey a 1m area using an automated lawnmower pattern. The drone will take and display an image at each stop. \
      <br/><br/><b>** Starting at the bottom left corner **</b>" 
    },
    {
      name: "Lawnmower Mission (5m)",
      enabled: true,
      
      img: "img_avatar2.png",
      link:"runMission.py&p1=flyLawnmower&p2=5&p3=5",
      
      description:"Survey a 5m square",
      tags:["test", "prebuilt", "lawnmower"],
      
      long_description:
      "Test our systems with a quick pre-built mission! \
      <br/><br/>The drone will survey a 5m area using an automated lawnmower pattern. The drone will take and display an image at each stop. \
      <br/><br/><b>** Starting at the bottom left corner **</b>"
    },
    {
      name: "Yolo Mission",
      enabled: true,
      
      img: "img_avatar2.png",
      link:"runMission.py&p1=flyYolo&p2=Yolo",
      
      description:"Detect objects using Yolov5!",
      tags:["prebuilt", "model", "yolo", "yolov5"],
      
      long_description:
      "Detect objects in your stream using Yolov5. The drone will capture an image and run inference using Yolov5. The drone an image drawing a bounding box along with confidence levels for every object detected in the image.",
    },
    {
      name: "GPS Square Mission",
      enabled: true,
      
      img: "img_avatar2.png",
      link:"runMission.py&p1=flyWaypointSquare&p2=20",
    
      description:"Use GPS to fly in a 20ft square",
      tags:["prebuilt", "waypoint", "square"],
      
      long_description:
      "The drone will use GPS to fly in a 20ft square.\
      <br/><br/><b>** Starting at the bottom left corner **</b> \
      <br/><b>** Must be flown outside **</b>",
    },
    {
      name: "GPS Lawnmower Mission",
      enabled: true,
      
      img: "img_avatar2.png",
      link:"runMission.py&p1=flyWaypointLawnmower&p2=0.02&p3=20&p4=10",

      description:"Use GPS to survey a 20ft square",
      tags:["prebuilt", "waypoint", "lawnmower"],
      
      long_description:
      "The drone will use GPS to survey a 20ft square area using an automated lawnmower pattern. The drone will take and display an image at each stop. \
      <br/><br/><b>** Starting at the bottom left corner **</b> \
      <br/><b>** Must be flown outside **</b>",
    },
    {
      name: "Custom Mission",
      enabled: true,
      
      img: "img_avatar2.png",
      link:"mission.py&p1=demomission",
      
      description:"Program your own custom mission!",
      tags:["custom"],
      
      long_description:
      "Program your own custom mission! Set your drone commands on our interactive platform and watch the drone fly.\
      <br/><br/> Setup: \
      <br/>  1) Enter your commands \
      ",
    },
    {
      name: "Custom GPS Mission",
      enabled: true,
      
      img: "img_avatar2.png",
      link:"mission.py&p1=waypointmission",
      description:"Set your coordinates and survey!",
      tags:["custom", "waypoint", "lawnmower"],
      
      long_description:"Set your field GPS boundaries with our interactive map and send the drone to survey the area. The drone will trace a lawnmower pattern over the selected field and return aerial images of the entire field. \
      <br/><br/> Setup: \
      <br/>  1) Use the interactive map to setup your field GPS boundaries. \
      <br/><br/><b>** Must be flown outside **</b>",
    },
    /*
    {
      name: "Stop Mission",
      
      img: "img_avatar2.png",
      link:"MainPage.py",
      
      description:"TODO: populate this",
      tags:["TODO"],
      
      long_description:
      "TODO: populate this",
    },
    */
];