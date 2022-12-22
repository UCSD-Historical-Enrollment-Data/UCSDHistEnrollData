# separate_grad_courses
A Rust program designed to separate each **raw** CSV files in the `holding` folder into two **raw** CSV files: one raw CSV file containing just graduate courses, and another containing just undergraduate courses.

## Usage
In the same directory that this executable is located, you should also have two directories: `holding`, and `split`. 

`holding` is where all CSV files should go for processing. `split` is where all CSV files will end up after processing. 

In terms of command usage:
```
./separate_grad_courses <ug term> <g term>
```
where
- `<ug term>` is the undergraduate term,
- `<g term>` is the graduate term.

This should be executed in the project's root directory.
