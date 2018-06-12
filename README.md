# snapdash

This code was tested using:
* ElasticSearch 5.4.0
* Kibana 5.1.1-SNAPSHOT


## Requirements

Code is compatible with Python 3, older versions are not supported.

We are going to use Chrome Headless mode, so version >=59 of Chrome web browser
is needed.

Chromedriver is also needed, you can download latest version from:
https://sites.google.com/a/chromium.org/chromedriver/home

You'll get a zip file containing a binary called `chromedriver`. Just extract
it and move it to your PATH. If you are using a Python virtual environment,
you can move it to your `venv/bin` path. To check your setup execute:
```
(venv) ➜  snapdash git:(master) ✗ chromedriver
Starting ChromeDriver 2.40.565383 (76257d1ab79276b2d53ee976b2c3e3b9f335cde7) on port 9515
Only local connections are allowed.

```

## Use Cases

### UC 1: Dashboard Snapshot
#### Description
Get a file with a dashboard snapshot.
```
snapdash &lt;url> &lt;image_name> [--start-date &lt;date> --end-date &lt;date>]
```
* **`url`**: dashboard URL.
* **`image_name`**: desired output image name.
* **`--start-date`**: date to retrieve data from. If not specified, dashboard 
    default time frame will be used.
* **`--end-date`**: date to retrieve data to. Defaults to now and has no effect if
    **`--start-date`** is not specified.

#### Requirements
* Access to Kibana non-editable version.

### UC 2: Visualization from URL
#### Description
Get a file with a single visualization given its URL, e.g.:
`http://localhost:5601/app/kibana#/visualize/edit/discourse_categories`
```
snapdash &lt;url> &lt;image_name> [--start-date &lt;date> --end-date &lt;date>]
```

Arguments are the same as in [UC 1: Dashboard Snapshot](#uc-1:-dashboard-snapshot).
`snapdash` should capture only visualization canvas.

#### Requirements
* Access to Kibana editable version.

### UC 3: Visualization from a Dashboard
#### Description
Get a file with a specified visualization from a Dashboard.
```
snapdash &lt;url> &lt;image_name> --viz &lt;viz_id> [--start-date &lt;date> --end-date &lt;date>]
```
* **`url`**: dashboard URL.
* **`image_name`**: desired output image name.
* **`--viz`**: identifier of the visualization we want to get a snapshot from. 
* **`--start-date`**: date to retrieve data from. If not specified, dashboard 
    default time frame will be used.
* **`--end-date`**: date to retrieve data to. Defaults to now and has no effect if
    **`--start-date`** is not specified.

#### Requirements
* Access to Kibana non-editable version.

## References
  * [Running Selenium wiyh headless Chrome](https://intoli.com/blog/running-selenium-with-headless-chrome/)
  * [How to take full-page screenshots with Selenium and Google Chrome in Ruby](https://gist.github.com/elcamino/5f562564ecd2fb86f559)