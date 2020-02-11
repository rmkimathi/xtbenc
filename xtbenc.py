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
        [sg.Combo(values=cpu, default_value='-c:v libx264 -preset superfast -crf 28 -g 25', size=(131, 1), key='_editor_')]
    ], title='Extra Options (after input):')],
    
    [sg.Button('ffprobe_in'),
     sg.Button('ffprobe_out')],
    
    [sg.Frame(layout=[
        [sg.Output(size=(130, 20))]], title='LOG')],
    
    [sg.Button('Convert'),
     sg.SimpleButton('Exit', button_color=('white','firebrick3'))]
]


window = sg.Window('XTB Encoder')

window.Layout(layout)


# Loop taking in user input

while True:

	(event, values) = window.Read(timeout=10)

	#print(event, values) #debug

	if event is 'Exit' or event is None:

		break           # Exit button clicked



	video_in = values['_infile_']
	video_out = values['_outfile_']

	args1 = "ffmpeg -v verbose -y -i"
	args2 = "ffmpeg -v verbose -y -vaapi_device ':0' -i"

	myargs = values['_editor_']

	ffp2 = ['ffprobe', '-hide_banner', video_in]
	ffp5 = ['ffprobe', '-hide_banner', video_out]


	cmd1 = [] # Radio button selection

	if values['_CPU'] == True: cmd1 = args1 + " " + "'%s'"%video_in + " " + myargs + " " + "'%s'"%video_out

	if values['_QSV'] == True: cmd1 = args1 + " " + "'%s'"%video_in + " " + myargs + " " + "'%s'"%video_out

	if values['_VAAPI'] == True: cmd1 = args2 + " " + "'%s'"%video_in + " " + myargs + " " + "'%s'"%video_out

	if values['_NVENC'] == True: cmd1 = args1 + " " + "'%s'"%video_in + " " + myargs + " " + "'%s'"%video_out


	cmd2 = shlex.split(cmd1)


	if event is '_CPU': window['_editor_'].Update(values=cpu, set_to_index=0)

	if event is '_QSV': window['_editor_'].Update(values=qsv, set_to_index=0)

	if event is '_VAAPI': window['_editor_'].Update(values=vaapi, set_to_index=0)

	if event is '_NVENC': window['_editor_'].Update(values=nvenc, set_to_index=0)



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



	if event is 'ffprobe_in':

		print('MEDIA INFO (Input):')

		ffp1 = subprocess.Popen(ffp2, stderr=subprocess.PIPE, universal_newlines=True)

		ffp3 = ffp1.communicate()[1]

		print(ffp3)



	if event is 'ffprobe_out':

		print('MEDIA INFO (Output):')

		ffp4 = subprocess.Popen(ffp5, stderr=subprocess.PIPE, universal_newlines=True)

		ffp6 = ffp4.communicate()[1]

		print(ffp6)



	if event is 'Convert':

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
