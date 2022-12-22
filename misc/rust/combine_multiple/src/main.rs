use std::{
    collections::{hash_map, HashMap},
    env,
    ffi::OsString,
    fs::{self, File, OpenOptions},
    io::{self, Write},
    path::{Path, PathBuf},
};

use hash_map::Entry;

fn main() -> io::Result<()> {
    let args = env::args().collect::<Vec<_>>();
    if args.len() <= 2 {
        println!("You need at least two term folders *and* the target term folder!");
        return Ok(());
    }

    let mut valid_overall: Vec<PathBuf> = vec![];
    let mut valid_section: Vec<PathBuf> = vec![];
    // Check if the term folders exist
    for arg in &args[..(args.len() - 1)] {
        let base_term_folder = Path::new(arg);
        if !base_term_folder.exists() {
            println!("Term folder '{}' doesn't exist! Exiting.", arg);
            return Ok(());
        }

        let base_overall = base_term_folder.join("overall");
        let base_section = base_term_folder.join("section");

        if base_overall.exists() {
            valid_overall.push(base_overall);
        }

        if base_section.exists() {
            valid_section.push(base_section);
        }
    }

    let target_term = &args[args.len() - 1];
    if !Path::new(target_term).exists() {
        fs::create_dir(target_term)?;
    }

    let target_overall = Path::new(target_term).join("overall");
    let target_section = Path::new(target_term).join("section");
    if !target_overall.exists() {
        fs::create_dir(&target_overall)?;
    }

    if !target_section.exists() {
        fs::create_dir(&target_section)?;
    }

    // Merge all terms
    // To do this, we'll have a map where the KEY is the course
    // and the VALUE is the new file itself
    for (target, valid) in &[
        (target_overall, valid_overall),
        (target_section, valid_section),
    ] {
        let mut map = HashMap::<OsString, File>::new();
        for o in valid {
            // get all files in this specific term's overall folder
            for f in fs::read_dir(o)? {
                let cleaned_csv = f?;
                let result_file = if let Entry::Vacant(e) = map.entry(cleaned_csv.file_name()) {
                    let mut this_file = OpenOptions::new()
                        .read(true)
                        .write(true)
                        .create(true)
                        .truncate(true)
                        .open(target.join(cleaned_csv.file_name()))?;
                    writeln!(this_file, "time,enrolled,available,waitlisted,total")?;
                    e.insert(this_file)
                } else {
                    map.get_mut(&cleaned_csv.file_name()).unwrap()
                };

                // With the result_file, write everything EXCEPT the first line (the CSV header)
                fs::read_to_string(cleaned_csv.path())?
                    .lines()
                    .skip(1)
                    .for_each(|line| writeln!(result_file, "{}", line).unwrap());
            }
        }
    }

    Ok(())
}
