# separate_grad_courses
A Rust program designed to separate each **raw** CSV files in the root `_holding` folder into two **raw** CSV files: one raw CSV file containing just graduate courses, and another containing just undergraduate courses.

## Usage
```
./separate_grad_courses <base folder> <ug folder> <g folder>
```
where
- `<base folder>` is the folder containing the data to separate,
- `<ug folder>` is the folder to put all undergraduate data in. This cannot be the same as `base_folder`.
- `<g folder>` is the folder to put all graduate data in. This cannot be the same as `base_folder`.

This should be executed in the project's root directory.
