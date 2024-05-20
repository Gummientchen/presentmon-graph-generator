# PresentMon-Grapher

This tool helps visualize PresentMon logs.

## Basic usage:

| Option | Long Option | Description                                                                         |
| ------ | ----------- | ----------------------------------------------------------------------------------- |
| -h     |             | Shows the integrated help                                                           |
| -i     | -Input      | Specifies the input .csv file from PresentMon                                       |
| -o     | -Output     | Specifies a custom output path. Must be .png                                        |
| -t     | -Title      | Set custom title which is shown at the top of generated image                       |
| -b     | -Bins       | Defines how many bins should be used for histograms                                 |
| -d     | -Theme      | Lets you choose between dark and light mode. Default dark. Options: "dark", "light" |
| -p     | -Pdf        | Exports the graph as a .pdf too                                                     |
| -v     | -Svg        | Exports the graph as a .svg too                                                     |

## Examples

```cmd
PresentMon-Grapher.exe -i "presentmon-log.csv"
```

### Define Output Path

```cmd
PresentMon-Grapher.exe -i "C:\presentmon-log.csv" -o "C:\presentmon-log.png"
```

### Set Number of Bins

```cmd
PresentMon-Grapher.exe -i "C:\presentmon-log.csv" -b 40
```

### Light Mode

```cmd
PresentMon-Grapher.exe -i "C:\presentmon-log.csv" -d light
```

### Export PDF too

```cmd
PresentMon-Grapher.exe -i "C:\presentmon-log.csv" -p
```

### Export SVG too

```cmd
PresentMon-Grapher.exe -i "C:\presentmon-log.csv" -v
```

### All Options Combined

```cmd
PresentMon-Grapher.exe -i "C:\presentmon-log.csv" -o "C:\presentmon-log.png" -b 40 -d light -p -v
```
