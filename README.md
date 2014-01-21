humimon
=======

This project provides both real-time monitoring/alerting of temperature and humidity as well as a simple web interface for viewing this in a graphical manner. For those of us with humidors without a glass case knowing what the current temp or rh levels is difficult without opening the lid and checking and also causing fluctuations in these values. Also, without keeping an eye on these values all the time manually you run the risk of dead sticks due to drying out or beetles. Hopefully this makes that risk much less by providing a way to monitor all the time and alert when values go out of range.

The current version is based off using either a DHT11, DHT22 or AM2302 sensor which can be found on the [Adafruit](https://www.adafruit.com/) website. In my own setup this is running well off a raspberry pi and an AM2302.

The web interface relies on AdvancedHTTPServer, found at https://gist.github.com/zeroSteiner/4502576 but can easily be adapted to utilize other projects such as Bottle or even the BaseHTTPServer.
