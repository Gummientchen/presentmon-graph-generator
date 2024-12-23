# PresentMon-Grapher

This tool helps visualize PresentMon logs.

![Example of the generated PNG](/assets/screenshot2.png)

## Features

- Generates graphs for PresentMon logs
- Shows basic stats like average FPS, max FPS, min FPS and percentiles
- Estimates the "smoothness" of a recorded game session
- Based on recorded logs gives an estimation if game is CPU or GPU limited
- Graphs for input latency to check your sanity

## Basic usage:

| Option | Long Option       | Description                                                                         |
| ------ | ----------------- | ----------------------------------------------------------------------------------- |
| -h     |                   | Shows the integrated help                                                           |
| -i     | -Input            | Specifies the input .csv file from PresentMon                                       |
| -o     | -Output           | Specifies a custom output path. Must be .png                                        |
| -t     | -Title            | Set custom title which is shown at the top of generated image                       |
| -b     | -Bins             | Defines how many bins should be used for histograms                                 |
| -d     | -Theme            | Lets you choose between dark and light mode. Default dark. Options: "dark", "light" |
| -p     | -Pdf              | Exports the graph as a .pdf too                                                     |
| -v     | -Svg              | Exports the graph as a .svg too                                                     |
| -f     | -DisableFiltering | Disables filtering on latency graphs                                                |

## Examples

### Basic usage with default settings

```cmd
PresentMon-Grapher.exe -i "presentmon-log.csv"
```

### Define Output Path

```cmd
PresentMon-Grapher.exe -i "C:\presentmon-log.csv" -o "C:\presentmon-log.png"
```

### Set Number of Bins

By default histograms use 40 bins. This can be changed with this option.

```cmd
PresentMon-Grapher.exe -i "C:\presentmon-log.csv" -b 40
```

### Light/Dark Mode

Allows you to switch between dark (default) and light mode. Light mode is better if you want to print the results.

```cmd
PresentMon-Grapher.exe -i "C:\presentmon-log.csv" -d light
```

```cmd
PresentMon-Grapher.exe -i "C:\presentmon-log.csv" -d dark
```

### Export PDF

```cmd
PresentMon-Grapher.exe -i "C:\presentmon-log.csv" -p
```

### Export SVG

```cmd
PresentMon-Grapher.exe -i "C:\presentmon-log.csv" -v
```

### Disable latency graph filtering

By default all latency graphs are filtered for better clarity. It tries to filter out extrem outliers. Those outliers usually happen while the game is loading a new level.

```cmd
PresentMon-Grapher.exe -i "C:\presentmon-log.csv" -f
```

### All Options Combined

```cmd
PresentMon-Grapher.exe -i "C:\presentmon-log.csv" -o "C:\presentmon-log.png" -b 40 -d light -p -v -f
```
