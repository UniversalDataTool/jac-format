# JAC (JSON as CSV) Format

The JAC format makes it easy to convert to and from JSON and CSV file formats, while giving application developers a lot of flexibility to customize how easy it is to modify the CSV file for end users. Any JSON object can be represented as a JAC CSV.

`.jac.csv` files are always valid CSVs.

An example JAC file is shown below:

| path      | .    | name  | dogs.0     | dogs.1   |
| --------- | ---- | ----- | ---------- | -------- |
| myName    | John |       |            |          |
| friends.0 |      | Stacy | Rufus      |          |
| friends.1 |      | Paul  | Mr. Fluffs | Whimpers |

When this file is converted into JSON, it becomes:

```javascript
{
  "myName": "John",
  "friends": [
    {
      "name": "Stacy",
      "dogs": ["Rufus"]
    },
    {
      "name": "Paul",
      "dogs": ["Mr. Fluffs", "Whimpers"]
    }
  ]
}
```

## Usage with Javascript

`npm install jac-format`

```javascript
const JAC = require("jac-format")

let csvString = JAC.toCSV(
  {
    fruit: [{ name: "apple" }, { name: "lemon" }],
  },
  {
    rows: ["fruit.0", "fruit.1"], // optional
    columns: ["name"], // optional
  }
)
// "path,name\r\nfruit.0,apple\r\nfruit.1,lemon"
// ┌───┬───────────┬─────────┐
// │   │     A     │    B    │
// ├───┼───────────┼─────────┤
// │ 1 │  'path'   │ 'name'  │
// │ 2 │ 'fruit.0' │ 'apple' │
// │ 3 │ 'fruit.1' │ 'lemon' │
// └───┴───────────┴─────────┘

// You can also use this
JAC.toJSON(csvString)
// > { "fruit": [{ "name": "apple" }, { "name": "lemon" }] }

// JAC.fromCSV === JAC.toJSON
// JAC.fromJSON === JAC.toCSV
```

## Usage with Python

`pip install jac_format`

```python
import jac_format as jac

csv_string = jac.to_csv(
  {
    "fruit": [{ "name": "apple" }, { "name": "lemon" }],
  },
  rows=["fruit.0", "fruit.1"],
  columns=["name"]
)

# > csv_string
# "path,name\r\nfruit.0,apple\r\nfruit.1,lemon"
# ┌───┬───────────┬─────────┐
# │   │     A     │    B    │
# ├───┼───────────┼─────────┤
# │ 1 │  'path'   │ 'name'  │
# │ 2 │ 'fruit.0' │ 'apple' │
# │ 3 │ 'fruit.1' │ 'lemon' │
# └───┴───────────┴─────────┘

jac.to_json(csv_string)
# { "fruit": [{ "name": "apple" }, { "name": "lemon" }] }
```

## Rules

- JAC CSV files are valid [RFC4180 CSVs](https://tools.ietf.org/html/rfc4180)
- `jac_csv_path` or `path` is the first column, first cell
- The first column contains the first path segment (except for the `jac_csv_path` cell)
- The first row (header) contains the second path segment (except for the `jac_csv_path` cell)
- Each value cell of a JAC CSV can be
  - 1. an empty cell
  - 2. a string
  - 3. a JSON object
  - 4. null
  - 5. a number
  - 7. a JSON array
- Columns right of the "path" column are applied in order from left to right. Each row creates an object. This object is then set at the path of the first column.
- A path can be traversed with either square bracket notation or dot notation
- In dot notation, the usage of a number indicates the index of an array (`a["1"].0` is equivalent to `a["1"][0]`)
- If an array has undefined values, those values are set to `null`
- A value cell's path is constructed by taking the leftmost cell of of a row (in the path column) and appending the topmost header to it

## Automatic Indexing with "\*"

Automatic indexing makes it easier to add and delete rows because index numbers don't need to be adjusted.

These tables are equivalent when converted to JSON:

| path       | .    | name  | dogs.\*    | dogs.\*  |
| ---------- | ---- | ----- | ---------- | -------- |
| myName     | John |       |            |          |
| friends.\* |      | Stacy | Rufus      |          |
| friends.\* |      | Paul  | Mr. Fluffs | Whimpers |

| path      | .    | name  | dogs.0     | dogs.1   |
| --------- | ---- | ----- | ---------- | -------- |
| myName    | John |       |            |          |
| friends.0 |      | Stacy | Rufus      |          |
| friends.1 |      | Paul  | Mr. Fluffs | Whimpers |

If "\*" are replaced by the smallest index in the path segment that's not already taken. There are two appropriate syntaxes, "[\*]" or ".\*". For a row, only the path segments in the row are considered (i.e. the header is converted into indicies without any information from the `path` column).

You can also use the `*` to refer to the last object created matching the prefix preceding the star. The example below is equivalent to the two tables above.

| path              | .          | name  |
| ----------------- | ---------- | ----- |
| myName            | John       |       |
| friends.\*        |            | Stacy |
| friends.\*.dogs.0 | Rufus      |       |
| friends.\*        |            | Paul  |
| friends.\*.dogs.0 | Mr. Fluffs |       |
| friends.\*.dogs.1 | Whimpers   |       |

## Pros & Cons

1. The flexibility of the JAC CSV format allows applications that output JAC CSV to give the user CSV data in a "flattening" that is most convenient for the application i.e. Columns can be created to make it easy for the user to modify the data.
2. As a result of the flexibility in the JAC CSV format, one JSON file can have almost an infinite amount of CSV variations.
3. Column order matters because it determines how the CSV is merged back into JSON
