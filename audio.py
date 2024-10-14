from just_playback import Playback

class AudioPlayBack:
    playback : Playback
    def __init__(self, filename : str, loop: bool) -> None:
        """ Create AudioPlayBack"""
        self.playback = Playback()
        self.playback.load_file(filename)
        self.playback.loop_at_end(loop)

    def play(self):
        """ play from the beginning. """
        self.playback.play()

    def resume(self):
        """ resume playing from paused. """
        self.playback.resume()

    def pause(self):
        """ pause the playback."""
        self.playback.pause()

    def stop(self):
        """ stop the playback"""
        self.playback.stop()
