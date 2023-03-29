# pyenv virtualenv 3.11.1 replicate
# pyenv local replicate
# pip install replicate
# pip install pynecone
# pc init
# pc run

import replicate
import pynecone as pc
# Using Replicate API and Pynecone
# You need to export the Replicate API key as env variable

class State(pc.State):
    # These are the two state variables
    img_prompt: str = ""
    img_url: str = ""

    # I am not entirely sure we need this tbh but the Pynecone doc is a bit confusing. No harm in writing a setter.
    def set_prompt(self, text):
        self.img_prompt = text

    # So we are quite lucky here as the "output" of this API call is literally just a URL. No need to do any JSON processing.
    # We don't check if img_prompt has a value, though, something to be added.
    def get_image(self):
        output = replicate.run(
            "stability-ai/stable-diffusion:db21e45d3f7023abc2a46ee38a23973f6dce16bb082a930b0c49861f96d1e5bf",
            input={"prompt": self.img_prompt}
        )
        # Writing the image URL into the state variable so it's updated automatically.
        self.img_url = output

def index():
    # This is centered both vertically and horizontally, but it's not responsive
    return pc.center(
        # vstack so this is a column
        pc.vstack(
            pc.heading("Stable Diffusion Image Generator", font_size="2em"),
            # on_blur waits until the user finishes editing the text field (exits)
            # Clicking the button is exiting, but the text field can't handle "enter". Something to implement.
            pc.input(placeholder="Enter an image prompt...", on_blur=State.set_prompt),
            pc.button(
                "Generate image",
                color_scheme="green",
                border_radius="1em",
                width="80%",
                # On click we call the Replicate API
                on_click=State.get_image,
            ),
            pc.divider(),
            pc.image(
                # Don't need to update anything manually as img_url is a state variable.
                # However, we don't have an initial placeholder (something to fix)
                src=State.img_url,
                height="25em",
                width="25em",
            ),
        ),
        # Man I have no idea why everything is neatly in the center of the screen and not ugly stretched side to side,
        # considering "width" is 100% here. Something to check in Pynecone docs.
        width="100%",
        height="100vh",
        background="radial-gradient(circle at 22% 11%,rgba(62, 180, 137,.20),hsla(0,0%,100%,0) 19%),radial-gradient(circle at 82% 25%,rgba(33,150,243,.18),hsla(0,0%,100%,0) 35%),radial-gradient(circle at 25% 61%,rgba(250, 128, 114, .28),hsla(0,0%,100%,0) 55%)",
    )

# Just boilerplate Pynecone stuff
app = pc.App(state=State)
app.add_page(index)
app.compile()