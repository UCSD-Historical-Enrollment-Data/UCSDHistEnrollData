use std::{
    env,
    fs::{self, OpenOptions},
    io::Write,
    path::Path,
    process::ExitCode,
};

fn main() -> anyhow::Result<ExitCode> {
    let args = env::args().collect::<Vec<_>>();
    if args.len() != 3 {
        println!("Usage: ./separate_grad_courses <ug name> <g name>");
        return Ok(ExitCode::FAILURE);
    }

    let ug_term = &args[args.len() - 2];
    let g_term = &args[args.len() - 1];

    if ug_term == g_term {
        println!("the base term and ug/g term must be different.");
        return Ok(ExitCode::FAILURE);
    }

    // Idea: this executable should be run in the directory containing a folder called
    // "holding"; this folder will contain all CSV files that need to be split. Split
    // files will be put in a folder called "split" which is also located in the same
    // place as the executable.

    let import_path = Path::new("holding");
    let export_path = Path::new("split");

    // Separate all grad/undergrad courses into two files.
    for f in fs::read_dir(import_path)? {
        let f = f?;
        let f_name = f.file_name();
        let f_type = f.file_type()?;
        if f_type.is_dir() {
            continue;
        }

        let f_name = match f_name.to_str() {
            Some(s) => s,
            None => continue,
        };

        if !f_name.ends_with(".csv") || f_name.ends_with("_fixed.csv") {
            continue;
        }

        let base_name = get_base_name(f_name);
        let new_ug_name = format!("{}_{}.csv", base_name, ug_term);
        let new_g_name = format!("{}_{}.csv", base_name, g_term);

        let new_ug_file = export_path.join(new_ug_name);
        let new_g_file = export_path.join(new_g_name);

        println!("Processing: {}", f_name);

        let content = fs::read_to_string(f.path())?;
        let csv_header = match content.lines().next() {
            Some(s) => s,
            None => continue,
        };

        let mut undergrad_data = String::new();
        undergrad_data.push_str(csv_header);
        undergrad_data.push('\n');

        let mut grad_data = String::new();
        grad_data.push_str(csv_header);
        grad_data.push('\n');

        for line in content.lines().skip(1) {
            let subj_num = match line.split(',').nth(1) {
                Some(x) => x,
                None => continue,
            };

            let course_num = get_course_num(subj_num);

            if course_num < 200 {
                undergrad_data.push_str(line);
                undergrad_data.push('\n');
            } else {
                grad_data.push_str(line);
                grad_data.push('\n');
            }
        }

        let mut ug_f = OpenOptions::new()
            .read(true)
            .write(true)
            .create(true)
            .truncate(true)
            .open(new_ug_file)?;
        ug_f.write_all(undergrad_data.as_bytes())?;

        let mut g_f = OpenOptions::new()
            .read(true)
            .write(true)
            .create(true)
            .truncate(true)
            .open(new_g_file)?;
        g_f.write_all(grad_data.as_bytes())?;
    }

    // Clean up all processed CSV files
    for f in fs::read_dir(import_path)? {
        let path = f?.path();
        if let Some(s) = path.extension() {
            if s.to_ascii_lowercase() != "md" {
                fs::remove_file(path)?;
            }
        }
    }

    Ok(ExitCode::SUCCESS)
}

fn get_course_num(subj_num: &str) -> u32 {
    subj_num
        .split(' ')
        .nth(1)
        .unwrap()
        .chars()
        .filter(|x| x.is_ascii_digit())
        .map(|x| x.to_digit(10).unwrap())
        .fold(0, |acc, elem| acc * 10 + elem)
}

fn get_base_name(f: &str) -> &str {
    let last_underscore = f.rfind('_').unwrap();
    &f[..last_underscore]
}
