import argparse
import os

import requests
from bs4 import BeautifulSoup


class FontAwesomeIconFetcher:
    VALID_FAMILIES = ["classic", "duotone", "sharp", "sharp-duotone", "brands"]
    VALID_STYLES = ["solid", "regular", "light", "thin"]

    def __init__(self):
        self.version = self._extract_fontawesome_version()
        self.output_directory = self._create_output_directory()

    def _create_output_directory(self):
        script_directory = os.path.dirname(os.path.abspath(__file__))
        output_dir = os.path.join(script_directory, "output")
        os.makedirs(output_dir, exist_ok=True)
        return output_dir

    # Extract the current version of FontAwesome from the website
    def _extract_fontawesome_version(self):
        url = "https://fontawesome.com/"
        try:
            response = requests.get(url)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, "html.parser")
            link_tag = soup.find("link", {"rel": "stylesheet", "href": lambda href: href and "releases" in href})

            if link_tag:
                href = link_tag["href"]
                version = href.split("/releases/")[1].split("/")[0]
                print(f"FontAwesome version extracted: {version}")
                return version
            print("Error: Version link not found in the response.")
        except requests.RequestException as e:
            print(f"Failed to fetch the FontAwesome version: {e}")
        return None

    # Fetch and save the SVG icon based on provided parameters
    def fetch_icon(self, name, family, style=None):
        if not self.version:
            print("Exiting due to version extraction failure.")
            return

        style = self._determine_style(family, style)
        if not self._download_svg(family, style, name):
            if family not in ["brands", "duotone", "sharp-duotone"]:
                print(f"Attempting to fetch with 'brands' family. Ignoring style.")
                self._download_svg("brands", None, name)

    # Adjust the icon style based on family rules
    def _determine_style(self, family, style):
        if family in ["duotone", "sharp-duotone"]:
            print(f"Selected '{family}' family. Ignoring style.")
            return None
        if family in ["classic", "sharp"]:
            return style
        if family == "brands":
            print(f"Selected icon family '{family}'. Ignoring style.")
            return None
        return style

    # Download and save the SVG icon file
    def _download_svg(self, family, style, name):
        family_style_dir = os.path.join(self.output_directory, f"{family}-{style}" if style else family)
        os.makedirs(family_style_dir, exist_ok=True)

        svg_url = self._construct_svg_url(family, style, name)
        print(f"Requesting SVG from URL: {svg_url}")
        try:
            svg_response = requests.get(svg_url)
            svg_response.raise_for_status()

            svg_file_path = os.path.join(family_style_dir, f"{name}.svg")
            with open(svg_file_path, "wb") as svg_file:
                svg_file.write(svg_response.content)
            print(f"SVG successfully saved to '{svg_file_path}'.")
            return True
        except requests.HTTPError as http_err:
            print(f"Failed to retrieve the SVG from '{svg_url}'. Error: {http_err}")
        except Exception as e:
            print(f"An error occurred while downloading the SVG: {e}")
        return False

    # Construct the SVG URL based on family, style, and name
    def _construct_svg_url(self, family, style, name):
        base_url = f"https://site-assets.fontawesome.com/releases/{self.version}/svgs"
        if family == "classic":
            return f"{base_url}/{style}/{name}.svg"
        if family == "sharp-duotone":
            return f"{base_url}/sharp-duotone-solid/{name}.svg"
        if not style and family != "brands":
            print("No style selected, defaulting to 'solid'.")
            style = "solid"
        return f"{base_url}/{family}/{name}.svg" if family in ["brands", "duotone"] else f"{base_url}/{family}-{style}/{name}.svg"

    # Validate the input for icon family and style
    def validate_input(self, family, style):
        if family not in self.VALID_FAMILIES:
            raise ValueError(f"Invalid icon family '{family}'. Valid options are: {', '.join(self.VALID_FAMILIES)}.")

        if style and family not in ["brands", "duotone", "sharp-duotone"] and style not in self.VALID_STYLES:
            raise ValueError(f"Invalid icon style '{style}' for family '{family}'. Valid options are: {', '.join(self.VALID_STYLES)}.")


# Collect user input manually
def get_user_input(fetcher):
    name = input("Enter icon name (e.g., 'house'): ")

    family = None
    while family not in FontAwesomeIconFetcher.VALID_FAMILIES:
        family = input("Enter icon family (e.g., 'classic', 'duotone', 'sharp', 'sharp-duotone', 'brands'): ")
        try:
            fetcher.validate_input(family, None)
        except ValueError as e:
            print(e)

    style = None
    if family not in ["brands", "duotone", "sharp-duotone"]:
        while True:
            style = input("Enter icon style (e.g., 'solid', 'regular', 'light', 'thin'): ")
            try:
                fetcher.validate_input(family, style)
                break
            except ValueError as e:
                print(e)

    return name, family, style


# Main function to handle arguments and initiate the icon fetching process
def main():
    parser = argparse.ArgumentParser(
        description="Fetch any FontAwesome icon from the FontAwesome library.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument("name", nargs="?", type=str, help="Icon name (e.g., 'house')")
    parser.add_argument("family", nargs="?", type=str, choices=FontAwesomeIconFetcher.VALID_FAMILIES, help="Icon family")
    parser.add_argument("style", nargs="?", type=str, choices=FontAwesomeIconFetcher.VALID_STYLES, help="Icon style (not necessary for the families 'brands', 'duotone', and 'sharp-duotone')")

    args = parser.parse_args()
    fetcher = FontAwesomeIconFetcher()

    if args.name and args.family:
        name = args.name
        family = args.family
        style = args.style if args.family not in ["brands", "duotone", "sharp-duotone"] else None
    else:
        print("No arguments provided. Enter details manually.")
        name, family, style = get_user_input(fetcher)

    fetcher.fetch_icon(name, family, style)


if __name__ == "__main__":
    main()
