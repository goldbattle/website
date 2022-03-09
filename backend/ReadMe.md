
- `./backend/_make_favicon.sh` - Will convert the profile picture into a icon favicon file


- `./backend/_make_thumbnails.sh` - Converts all files in `downloads/images` into thumbnails.
This really isn't that important since we don't pay hosting costs, but will make the site load a lot faster.
Default size is 200x200 pixels, which seems to be reasonable.


- `python3 backend/generate_from_bibtex.py` - Takes in the citation file and generates html for the homepage.
This just makes it so that the bibtex file will contain all the information about each reference.
From that we can generate the links to videos and downloads as needed.


