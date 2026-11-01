use std::{env, error::Error, fs};

use git_koi::behavior::Behavior;
use git_koi::coat::KoiBody;
use git_koi::history::AccountSnapshot;
use git_koi::koi::derive_koi_development;
use git_koi::motion::frame_count;
use git_koi::output::encode_gif;
use git_koi::render::render_swim_frame;

fn main() -> Result<(), Box<dyn Error>> {
    let args: Vec<_> = env::args().collect();
    if args.len() != 3 {
        return Err("usage: profile-koi-cruise SNAPSHOT OUTPUT".into());
    }
    let snapshot: AccountSnapshot = serde_json::from_slice(&fs::read(&args[1])?)?;
    let koi = derive_koi_development(&snapshot)?;
    let frames: Vec<_> = (0..frame_count(Behavior::Cruise))
        .map(|i| render_swim_frame(&koi, KoiBody::Asagi, Behavior::Cruise, i))
        .collect();
    fs::write(&args[2], encode_gif(&frames)?)?;
    Ok(())
}
