<html>
<head>
        <meta name="viewport" content="width=device-width" />
        <title>Home Doorbell</title>
        <link href="mymain.css" rel="stylesheet" type="text/css">
</head>
<body>
        <div class="organize-pane">
                <div class="home-container">
                        <h1>Home Doorbell</h1>
                        <div class="home-text-container">
                                <form method="get" action="index.php">
                                        <label for="door">Door Control :</label>
                                        <input type="submit" style="font-size: 14 pt" value="OPEN" name="on_door">
                                        <label for="speaker">Speaker Control : </label>
                                        <input type="submit" style="font-size: 14 pt" value="ON" name="on_speaker">
					<label for="speaker">Livestreaming : </label>
					<a href= "livestreaming.html" class="button">See the person</a>
                                </form>​​​
                        </div>
	        </div>
        </div>

        <div class="img-pane">
               <!-- <iframe src="http://192.168.1.11/images/img1.jpg" width="300" height="300" name="Person"> </iframe>-->
		<img src="http://192.168.1.11/images/person.jpg" name="Person" srcset=" http://192.168.1.11/images/person.jpg 2000w, http://192.168.1.11/images/person.jpg 1000w" sizes="(min-width: 36em) 33.3vw, 100vw"> </img>
	</div>
                <?php
                        shell_exec("/usr/local/bin/gpio -g mode 27 out");
			shell_exec("/usr/local/bin/gpio -g mode 22 out");
			if(isset($_GET['on_door'])) {
                        echo "Door is open";
                        shell_exec("/usr/local/bin/gpio -g write 27 1");
			sleep(2);
			shell_exec("/usr/local/bin/gpio -g write 27 0");
                       	} else if(isset($_GET['on_speaker'])) {
                        echo "Speaker is on";
                        shell_exec("/usr/local/bin/gpio -g write 22 1");
			}
                ?>
</body>
</html>

