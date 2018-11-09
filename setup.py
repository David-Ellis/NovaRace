import cx_Freeze

executables = [cx_Freeze.Executable("NovaRace.py")]

cx_Freeze.setup(
	name = "Nova Race",
	options = {"build_exe": {"packages":["pygame","numpy"], "include_files":['car.png',
            'CarIcon.png','Choose.png','ChooseHover.png','GrassL.png','GrassR.png',
            'Logo.png','menuBG.png','music.png','musicHover.png','Off.png',
            'OffHover.png','On.png','OnHover.png','Options.png','OptionsHover.png',
            'otherCar1.png','otherCar2.png','otherCar3.png','Quit.png','QuitHover.png',
            'Return.png','ReturnHover.png','Start.png','StartHover.png','ding.wav',
            'click.wav','crash.wav','music.ogg','Logo.png']}},
	executables = executables

	)