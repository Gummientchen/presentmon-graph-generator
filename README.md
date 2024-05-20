# PresentMon-Grapher

This tool helps visualize PresentMon logs.

## Basic usage:

| Option | Long Option | Description                                                   |
| ------ | ----------- | ------------------------------------------------------------- |
| -h     |             | Shows the integrated help                                     |
| -i     | -Input      | Specifies the input .csv file from PresentMon                 |
| -o     | -Output     | Specifies a custom output path. Must be .png                  |
| -t     | -Title      | Set custom title which is shown at the top of generated image |
| -b     | -Bins       | Defines how many bins should be used for histograms           |

## Examples

```cmd
PresentMon-Grapher.exe -i "presentmon-log.csv"
```

```cmd
PresentMon-Grapher.exe -i "C:\presentmon-log.csv" -o "C:\presentmon-log.png"
```

```cmd
PresentMon-Grapher.exe -i "C:\presentmon-log.csv" -o "C:\presentmon-log.png" -b 40
```
