#!/usr/bin/env python3
# coding: utf-8



import PySimpleGUI as sg
import subprocess
import shlex
import csv


sg.ChangeLookAndFeel('LightGreen')


with open('presets/CPU.csv', newline='') as csvfile:
    spamreader = csv.reader(csvfile , delimiter=',', quotechar='"')
    for Tup1 in spamreader:
       cpu = (Tup1)


with open('presets/QSV.csv', newline='') as csvfile:
    spamreader = csv.reader(csvfile , delimiter=',', quotechar='"')
    for Tup2 in spamreader:
       qsv = (Tup2)


with open('presets/VAAPI.csv', newline='') as csvfile:
    spamreader = csv.reader(csvfile , delimiter=',', quotechar='"')
    for Tup3 in spamreader:
       vaapi = (Tup3)    


with open('presets/NVENC.csv', newline='') as csvfile:
    spamreader = csv.reader(csvfile , delimiter=',', quotechar='"')
    for Tup4 in spamreader:
       nvenc = (Tup4)


layout = [
    [sg.Text('Input', size=(7,1)),
     sg.InputText(key='_infile_', size=(116,1)),
     sg.FileBrowse(size=(8,1))],
    
    [sg.Text('Output', size=(7,1)),
     sg.InputText(key='_outfile_', size=(116,1)),
     sg.SaveAs(size=(8,1))],
    
    [sg.Frame(layout=[
        [sg.Radio('CPU', "RADIO1", default=True, key='_CPU', enable_events=True),
         sg.Radio('QSV', "RADIO1", key='_QSV', enable_events=True),
         sg.Radio('VAAPI', "RADIO1", key='_VAAPI', enable_events=True),
         sg.Radio('NVENC', "RADIO1", key='_NVENC', enable_events=True)]
    ], title='CODEC',title_color='red', relief=sg.RELIEF_SUNKEN, tooltip='Use these to set flags')],
    
    [sg.Frame(layout=[
        [sg.Combo(values=cpu, default_value='', size=(134, 20), auto_size_text=False, key='_editor_')]
    ], title='Extra Options (after input):')],
    
    [sg.Button('ffprobe_in'),
     sg.Button('ffprobe_out')],
    
    [sg.Frame(layout=[
        [sg.Output(size=(134, 20), font=("Consolas", 10))]], title='LOG')],
    
    [sg.Button('Convert'),
     sg.SimpleButton('Exit', button_color=('white','firebrick3'))]
]


window = sg.Window('XTB Encoder', icon='presets/xtbenc.png') # icon='presets/xtbenc.ico' for Windows

window.Layout(layout)


# Loop taking in user input

while True:

	(event, values) = window.Read(timeout=10)

	#print(event, values) #debug

	if event == 'Exit' or event is None:

		break           # Exit button clicked



	video_in = values['_infile_']
	video_out = values['_outfile_']

	args1 = "ffmpeg -v verbose -y -i"
	args2 = "ffmpeg -v verbose -y -vaapi_device '/dev/dri/renderD128' -i"

	myargs = values['_editor_']

	ffp1 = ['ffprobe', '-hide_banner', video_in]
	ffp2 = ['ffprobe', '-hide_banner', video_out]


	cmd1 = [] # Radio button selection

	if values['_CPU'] is True: cmd1 = args1 + " " + "'%s'"%video_in + " " + myargs + " " + "'%s'"%video_out

	if values['_QSV'] is True: cmd1 = args1 + " " + "'%s'"%video_in + " " + myargs + " " + "'%s'"%video_out

	if values['_VAAPI'] is True: cmd1 = args2 + " " + "'%s'"%video_in + " " + myargs + " " + "'%s'"%video_out

	if values['_NVENC'] is True: cmd1 = args1 + " " + "'%s'"%video_in + " " + myargs + " " + "'%s'"%video_out


	cmd2 = shlex.split(cmd1)


	if event == '_CPU': window['_editor_'].Update(values=cpu, set_to_index=0)

	if event == '_QSV': window['_editor_'].Update(values=qsv, set_to_index=0)

	if event == '_VAAPI': window['_editor_'].Update(values=vaapi, set_to_index=0)

	if event == '_NVENC': window['_editor_'].Update(values=nvenc, set_to_index=0)



	def invoke_process_popen_poll_live(command):

		process = subprocess.Popen(command,
                                   stdin=subprocess.DEVNULL,
                                   stdout=subprocess.DEVNULL,
                                   stderr=subprocess.PIPE,
                                   universal_newlines=True)

		while True:

			err = process.stderr.readline()

			# used to check for empty output in Python2, but seems

			# to work with just poll in 2.7.12 and 3.5.2

			#if errors == '' and process.poll() is not None:

			if process.poll() is not None:

				break

			if err:

				#print(output.strip().decode())

				print(err.strip())

				window.refresh()

		rc = process.poll()

		return rc    



	if event == 'ffprobe_in':

		print('MEDIA INFO (Input):')

		ffp3 = subprocess.Popen(ffp1, stderr=subprocess.PIPE, universal_newlines=True)

		ffp4 = ffp3.communicate()[1]

		print(ffp4)



	if event == 'ffprobe_out':

		print('MEDIA INFO (Output):')

		ffp5 = subprocess.Popen(ffp2, stderr=subprocess.PIPE, universal_newlines=True)

		ffp6 = ffp5.communicate()[1]

		print(ffp6)



	if event == 'Convert':

		print('INPUT:', video_in)

		print( )

		print('OUTPUT:', video_out)

		print( )

		print('ARGS:', cmd2)

		print( )

		window.refresh()

		invoke_process_popen_poll_live(cmd2)

		print( )

		print('**********     RESULT     **********')

		print( )



window.close()
