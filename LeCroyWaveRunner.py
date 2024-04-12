import time
import numpy as np
import pyvisa
import datetime
import struct
import warnings




TYPES_LENGTH_IN_LECROY_2_3 = {
	# This is in accordance with the specification in `LECROY_2_3:  TEMPLATE`, query the command `'TMPL?'` to a LeCroy oscilloscope for more information.
	'byte': 1,
	'word': 2,
	'long': 4,
	'float': 4,
	'enum': 2,
	'string': 16,
	'double': 8,
	'unit_definition': 48,
	'time_stamp': 16,
}

def parse_bytes_LECROY_2_3(raw_bytes:bytes, interpret_as:str):
	"""Parses an array of bytes according to the specification in the so
	called `LECROY_2_3 template`. 
	
	Arguments
	---------
	raw_bytes: array of bytes
		An array of bytes, hopefully created by a LeCroy oscilloscope.
	interpret_as: str
		How to interpret the bytes. Possible options are 'byte', 'word',
		'long', 'float', 'enum', 'string', 'double', 'unit_definition', 
		and 'time_stamp'.
	
	Returns
	-------
	parsed_bytes: variable type
		Returns the information extracted from the bytes in the appropriate
		Python type.
	"""
	# If you don't know what the `LECROY_2_3 template` is just query your oscilloscope the command `'TMPL?'` and it will answer a long text with all the information to understand this function.
	if len(raw_bytes) != TYPES_LENGTH_IN_LECROY_2_3[interpret_as]:
		raise ValueError(f'I was requested to interpret an array of bytes of length {len(raw_bytes)} as a {repr(interpret_as)}, but according to the specification in the `LECROY_2_3 template` a {repr(interpret_as)} requires exactly {TYPES_LENGTH_IN_LECROY_2_3[interpret_as]} bytes. ')
	if not isinstance(raw_bytes, bytes):
		raise TypeError(f'`raw_bytes` must be an instance of {repr(bytes)}, received an object of type {type(raw_bytes)}. ')
	
	if interpret_as in {'string','unit_definition'}:
		return raw_bytes.decode('ASCII').replace(b'\x00'.decode('ASCII'), '')
	elif interpret_as == 'byte':
		return int.from_bytes(raw_bytes, byteorder='big', signed=True)
	elif interpret_as == 'word':
		return int.from_bytes(raw_bytes, byteorder='big', signed=True)
	elif interpret_as == 'long':
		return int.from_bytes(raw_bytes, byteorder='big', signed=True)
	elif interpret_as == 'float':
		return struct.unpack('>f', raw_bytes)[0]
	elif interpret_as == 'double':
		return struct.unpack('>d', raw_bytes)[0]
	elif interpret_as == 'enum':
		return int.from_bytes(raw_bytes, byteorder='big', signed=False)
	elif interpret_as == 'time_stamp':
		seconds = struct.unpack('>d', raw_bytes[0:TYPES_LENGTH_IN_LECROY_2_3['double']])[0]
		return datetime.datetime(
			second = int(divmod(seconds,1)[0]),
			microsecond = int(divmod(seconds,1)[1]),
			minute = int.from_bytes(raw_bytes[TYPES_LENGTH_IN_LECROY_2_3['double']:TYPES_LENGTH_IN_LECROY_2_3['double']+1], byteorder='big'),
			hour = int.from_bytes(raw_bytes[TYPES_LENGTH_IN_LECROY_2_3['double']+1:TYPES_LENGTH_IN_LECROY_2_3['double']+2], byteorder='big'),
			day = int.from_bytes(raw_bytes[TYPES_LENGTH_IN_LECROY_2_3['double']+2:TYPES_LENGTH_IN_LECROY_2_3['double']+3], byteorder='big'),
			month = int.from_bytes(raw_bytes[TYPES_LENGTH_IN_LECROY_2_3['double']+3:TYPES_LENGTH_IN_LECROY_2_3['double']+4], byteorder='big'),
			year = int.from_bytes(raw_bytes[TYPES_LENGTH_IN_LECROY_2_3['double']+4:TYPES_LENGTH_IN_LECROY_2_3['double']+6], byteorder='big'),
		)
	else:
		raise ValueError(f'Dont know how to parse bytes of type {repr(interpret_as)}, supported types are {sorted(set(TYPES_LENGTH_IN_LECROY_2_3))}. ')

def parse_wavedesc_block(raw_bytes:bytes)->dict:
	"""Given an array of bytes, hopefully produced by a LeCroy oscilloscope,
	it parses the WAVEDESC block header. If you don't know what this header
	is, query `'TMPL?'` to a LeCroy oscilloscope and it will answer with
	a long text documenting this.
	
	Arguments
	---------
	raw_bytes: bytes
		The array of bytes produced by the LeCroy oscilloscope from which
		to parse the WAVEDESC block out.
	
	Returns
	-------
	parsed_header: dict
		A dictionary with the parsed data.
	"""
	WAVEDESC_HEADER_STRUCTURE = [
		# To get documentation about this header, query the command 'TMPL?' to a LeCroy oscilloscope.
		{
			'position': 0,
			'name': 'DESCRIPTOR_NAME',
			'type': 'string',
		},
		{
			'position': 16,
			'name': 'TEMPLATE_NAME',
			'type': 'string',
		},
		{
			'position': 32,
			'name': 'COMM_TYPE',
			'type': 'enum',
		},
		{
			'position': 34,
			'name': 'COMM_ORDER',
			'type': 'enum',
		},
		{
			'position': 36,
			'name': 'WAVE_DESCRIPTOR',
			'type': 'long',
		},
		{
			'position': 40,
			'name': 'USER_TEXT',
			'type': 'long',
		},
		{
			'position': 44,
			'name': 'RES_DESC1',
			'type': 'long',
		},
		{
			'position': 48,
			'name': 'TRIGTIME_ARRAY',
			'type': 'long',
		},
		{
			'position': 52,
			'name': 'RIS_TIME_ARRAY',
			'type': 'long',
		},
		{
			'position': 56,
			'name': 'RES_ARRAY1',
			'type': 'long',
		},
		{
			'position': 60,
			'name': 'WAVE_ARRAY_1',
			'type': 'long',
		},
		{
			'position': 64,
			'name': 'WAVE_ARRAY_2',
			'type': 'long',
		},
		{
			'position': 68,
			'name': 'RES_ARRAY2',
			'type': 'long',
		},
		{
			'position': 72,
			'name': 'RES_ARRAY3',
			'type': 'long',
		},
		{
			'position': 76,
			'name': 'INSTRUMENT_NAME',
			'type': 'string',
		},
		{
			'position': 92,
			'name': 'INSTRUMENT_NUMBER',
			'type': 'long',
		},
		{
			'position': 96,
			'name': 'TRACE_LABEL',
			'type': 'string',
		},
		{
			'position': 112,
			'name': 'RESERVED1',
			'type': 'word',
		},
		{
			'position': 114,
			'name': 'RESERVED2',
			'type': 'word',
		},
		{
			'position': 116,
			'name': 'WAVE_ARRAY_COUNT',
			'type': 'long',
		},
		{
			'position': 120,
			'name': 'PNTS_PER_SCREEN',
			'type': 'long',
		},
		{
			'position': 124,
			'name': 'FIRST_VALID_PNT',
			'type': 'long',
		},
		{
			'position': 128,
			'name': 'LAST_VALID_PNT',
			'type': 'long',
		},
		{
			'position': 132,
			'name': 'FIRST_POINT',
			'type': 'long',
		},
		{
			'position': 136,
			'name': 'SPARSING_FACTOR',
			'type': 'long',
		},
		{
			'position': 140,
			'name': 'SEGMENT_INDEX',
			'type': 'long',
		},
		{
			'position': 144,
			'name': 'SUBARRAY_COUNT',
			'type': 'long',
		},
		{
			'position': 148,
			'name': 'SWEEPS_PER_ACQ',
			'type': 'long',
		},
		{
			'position': 152,
			'name': 'POINTS_PER_PAIR',
			'type': 'word',
		},
		{
			'position': 154,
			'name': 'PAIR_OFFSET',
			'type': 'word',
		},
		{
			'position': 156,
			'name': 'VERTICAL_GAIN',
			'type': 'float',
		},
		{
			'position': 160,
			'name': 'VERTICAL_OFFSET',
			'type': 'float',
		},
		{
			'position': 164,
			'name': 'MAX_VALUE',
			'type': 'float',
		},
		{
			'position': 168,
			'name': 'MIN_VALUE',
			'type': 'float',
		},
		{
			'position': 172,
			'name': 'NOMINAL_BITS',
			'type': 'word',
		},
		{
			'position': 174,
			'name': 'NOM_SUBARRAY_COUNT',
			'type': 'word',
		},
		{
			'position': 176,
			'name': 'HORIZ_INTERVAL',
			'type': 'float',
		},
		{
			'position': 180,
			'name': 'HORIZ_OFFSET',
			'type': 'double',
		},
		{
			'position': 188,
			'name': 'PIXEL_OFFSET',
			'type': 'double',
		},
		{
			'position': 196,
			'name': 'VERTUNIT',
			'type': 'unit_definition',
		},
		{
			'position': 292,
			'name': 'HORIZ_UNCERTAINTY',
			'type': 'float',
		},
		{
			'position': 296,
			'name': 'TRIGGER_TIME',
			'type': 'time_stamp',
		},
		{
			'position': 312,
			'name': 'ACQ_DURATION',
			'type': 'float',
		},
		{
			'position': 316,
			'name': 'RECORD_TYPE',
			'type': 'enum',
		},
		{
			'position': 318,
			'name': 'PROCESSING_DONE',
			'type': 'enum',
		},
		{
			'position': 320,
			'name': 'RESERVED5',
			'type': 'word',
		},
		{
			'position': 322,
			'name': 'RIS_SWEEPS',
			'type': 'word',
		},
		{
			'position': 324,
			'name': 'TIMEBASE',
			'type': 'enum',
		},
		{
			'position': 326,
			'name': 'VERT_COUPLING',
			'type': 'enum',
		},
		{
			'position': 328,
			'name': 'PROBE_ATT',
			'type': 'float',
		},
		{
			'position': 332,
			'name': 'FIXED_VERT_GAIN',
			'type': 'enum',
		},
		{
			'position': 334,
			'name': 'BANDWIDTH_LIMIT',
			'type': 'enum',
		},
		{
			'position': 336,
			'name': 'VERTICAL_VERNIER',
			'type': 'float',
		},
		{
			'position': 340,
			'name': 'ACQ_VERT_OFFSET',
			'type': 'float',
		},
		{
			'position': 344,
			'name': 'WAVE_SOURCE',
			'type': 'enum',
		},
	]
	
	parsed_header = {}
	for element_structure in WAVEDESC_HEADER_STRUCTURE:
		element_bytes = raw_bytes[element_structure['position']:element_structure['position']+TYPES_LENGTH_IN_LECROY_2_3[element_structure['type']]]
		parsed_header[element_structure['name']] = parse_bytes_LECROY_2_3(element_bytes, element_structure['type'])
	if parsed_header['DESCRIPTOR_NAME'] != 'WAVEDESC':
		raise RuntimeError(f'Error parsing WAVEDESC header from raw bytes.')
	return parsed_header

def parse_data_array_1_block(raw_bytes:bytes, parsed_wavedesc_block:dict)->list:
	"""Given an array of bytes, hopefully produced by a LeCroy oscilloscope,
	it parses the DATA_ARRAY_1 block. If you don't know what this 
	is, query `'TMPL?'` to a LeCroy oscilloscope and it will answer with
	a long text documenting this.
	
	Arguments
	---------
	raw_bytes: bytes
		The array of bytes produced by the LeCroy oscilloscope from which
		to parse the WAVEDESC block out.
	parsed_wavedesc_block: dict
		The dictionary produced by the `parsed_wavedesc_block` function.
	
	Returns
	-------
	samples: list of float
		A list with the samples in the oscilloscope in units of volt (or
		whatever unit they have), and with `float('NaN')` values in those
		samples where there was overflow.
	"""
	wave_data_start_position = parsed_wavedesc_block['WAVE_DESCRIPTOR'] + parsed_wavedesc_block['USER_TEXT'] + parsed_wavedesc_block['TRIGTIME_ARRAY'] + parsed_wavedesc_block['RIS_TIME_ARRAY']
	wave_data_stop_position = wave_data_start_position+parsed_wavedesc_block['WAVE_ARRAY_1']
	wave_raw_data = raw_bytes[wave_data_start_position:wave_data_stop_position]
	grouped_raw_data = [wave_raw_data[2*i:2*i+2] for i in range(int(len(wave_raw_data)/2))]
	samples = [parse_bytes_LECROY_2_3(group_of_raw, 'word') for group_of_raw in grouped_raw_data] # Bytes to integers.
	samples = [s if parsed_wavedesc_block['MIN_VALUE']<=s<=parsed_wavedesc_block['MAX_VALUE'] else float('NaN') for s in samples] # Overflow check.
	samples = [s*parsed_wavedesc_block['VERTICAL_GAIN'] - parsed_wavedesc_block['VERTICAL_OFFSET'] for s in samples] # ADC to Volts conversion.
	return samples

def parse_trigtime_block(raw_bytes:bytes, parsed_wavedesc_block:dict)->list:
	"""Given an array of bytes, hopefully produced by a LeCroy oscilloscope,
	it parses the TRIGTIME block. If you don't know what this means just
	query `'TMPL?'` to a LeCroy oscilloscope and it will answer with
	a long text documenting this.
	
	Arguments
	---------
	raw_bytes: bytes
		The array of bytes produced by the LeCroy oscilloscope from which
		to parse the WAVEDESC block out.
	parsed_wavedesc_block: dict
		The dictionary produced by the `parsed_wavedesc_block` function.
	
	Returns
	-------
	parsed_trigtime_block: list of dict
		A list with the parsed trigtime for each of the acquired sequences.
		Each element of the list corresponds to each of the sequences
		acquired by the oscilloscope.
		If the TRIGTIME block is non existent (e.g. the oscilloscope was
		in RealTime instead of Sequence timebase, an empty list is returned.
	"""
	TRIGTIME_BLOCK_STRUCTURE = [
		# To get documentation about this header, query the command 'TMPL?' to a LeCroy oscilloscope.
		{
			'position': 0,
			'name': 'TRIGGER_TIME',
			'type': 'double',
		},
		{
			'position': 8,
			'name': 'TRIGGER_OFFSET',
			'type': 'double',
		},
	]
	TRIGTIME_BLOCK_LENGTH_SINGLE_SUBARRAY = sum([TYPES_LENGTH_IN_LECROY_2_3[element['type']] for element in TRIGTIME_BLOCK_STRUCTURE])
	
	if parsed_wavedesc_block['TRIGTIME_ARRAY'] == 0: # This means that there is no TRIGTIME bock to parse, probably because the oscilloscope was not configured in SEQUENCE mode.
		return []
	
	trigtime_block_start_position = parsed_wavedesc_block['WAVE_DESCRIPTOR'] + parsed_wavedesc_block['USER_TEXT']
	trigtime_block_stop_position = parsed_wavedesc_block['WAVE_DESCRIPTOR'] + parsed_wavedesc_block['USER_TEXT'] + parsed_wavedesc_block['TRIGTIME_ARRAY']
	trigtime_block_bytes = raw_bytes[trigtime_block_start_position:trigtime_block_stop_position]
	
	parsed_trigtime_block = []
	for i in range(parsed_wavedesc_block['SUBARRAY_COUNT']):
		parsed_header = {}
		for element_structure in TRIGTIME_BLOCK_STRUCTURE:
			element_bytes = trigtime_block_bytes[i*TRIGTIME_BLOCK_LENGTH_SINGLE_SUBARRAY+element_structure['position']:i*TRIGTIME_BLOCK_LENGTH_SINGLE_SUBARRAY+element_structure['position']+TYPES_LENGTH_IN_LECROY_2_3[element_structure['type']]]
			parsed_header[element_structure['name']] = parse_bytes_LECROY_2_3(element_bytes, element_structure['type'])
		parsed_trigtime_block.append(parsed_header)
	return parsed_trigtime_block

class WaveRunner:
	def __init__(self, resource_name:str):
		try:
			rm = pyvisa.ResourceManager('@py')
			self.resource = rm.open_resource(resource_name)
		except:
				print('Pyvisa not installed')
				raise
		self.ch1= self.Channel(self.resource,1)
		self.ch2= self.Channel(self.resource,2)
		self.ch3= self.Channel(self.resource,3)
		self.ch4= self.Channel(self.resource,4)
		self.write('CHDR OFF') # This is to receive only numerical data in the answers and not also the echo of the command and some other stuff. See p. 22 of http://cdn.teledynelecroy.com/files/manuals/tds031000-2000_programming_manual.pdf

		def tdiv(self, tdiv: str):
			"""Sets the horizontal scale per division for the main window.
			Parameterers
			------------
			 '1NS','2NS','5NS','10NS','20NS','50NS','100NS','200NS','500NS',
			 '1US','2US','5US','10US','20US','50US','100US','200US','500US',
			 '1MS','2MS','5MS','10MS','20MS','50MS','100MS','200MS','500MS',
			 '1S','2S','5S','10S','20S','50S','100S' 
			"""
			divisions=[ 1, 2, 10, 20, 50, 100,
						1e-3,2e-3,5e-3,10e-3,20e-3,50e-3,100e-3,200e-3,500e-3,
						1e-6,2e-6,5e-6,10e-6,20e-6,50e-6,100e-6,200e-6,500e-6,
						1e-9,2e-9,5e-9,10e-9,20e-9,50e-9,100e-9,200e-9,500e-9]
			
			closestValue = max(divisions, key=lambda x: abs(x - (tdiv/10)))
			
			# See https://cdn.teledynelecroy.com/files/manuals/maui-remote-control-and-automation-manual.pdf#page=233
			self._osc.write(f'TDIV {closestValue}')

	def idn(self):
		"""Returns the name of the instrument, i.e. its answer to the
		command "*IDN?"."""
		return  self.query('*IDN?')
	
	def close(self):
		self.resource.close()

	def write(self, msg):
		"""Sends a command to the instrument."""
		self.resource.write(msg)
	
	def read(self):
		"""Reads the answer from the instrument."""
		response = self.resource.read()
		if response[-1] == '\n':
			response = response[:-1]
		return response
	
	def query(self, msg):
		return 	self.resource.query(msg)
	
	def waitTrigger(self):
		self.write('WAIT')
	def opComplete(self):
		while int(self.query('*OPC?')) != 1:
			print(len(self.query('*OPC?')))
			time.sleep(.1)
	@property
	def trigMode(self):
		return self.query('TRMD?')
	
	@trigMode.setter
	def trigMode(self, mode: str):
		# See https://cdn.teledynelecroy.com/files/manuals/tds031000-2000_programming_manual.pdf#page=152
		"""Sets the trigger mode.
		Parameterers
		------------
			mode : str
			AUTO,NORM,SINGLE,STOP
			• NORM — When NORMAL If the trigger signal is satisfied,
			the running state shows Trig'd, and the interface shows
			stable waveform.
			Otherwise, the running state shows Ready, and
			the interface displays the last triggered
			waveform (previous trigger) or does not
			display the waveform (no previous trigger)
			• SINGLE —If the trigger signal is satisfied, the running
			state shows Trig'd, and the interface shows
			stable waveform. Then, the oscilloscope stops
			scanning, the RUN/STOP key is red light, and
			the running status shows Stop.
		"""
		self.write(f'TRMD {mode}')


	
	def trigSelect(self,trig_type:str , trig_source: str):
		"""Sets the trigger conditions
		Parameterers
		------------
		trig_type: str
		Dropout:DROP,Edge:EDGE,GLIT,Single-source:SNG,Standard:STD
		trig_source : str
		C1,C2,C3,C4,EX,EX5
		  """
		# See https://cdn.teledynelecroy.com/files/manuals/maui-remote-control-and-automation-manual.pdf#page=241
		self.write(f'TRIG_SELECT {trig_type},SR,{trig_source} ')

	@property
	def trigCoupling(self):
		return self.query('TRIG_COUPLING?')

	@trigCoupling.setter
	def trigCoupling(self, trig_source: str, trig_coupling: str):
		"""Set the trigger coupling .
			Parameterers
			------------
			trig_source : str
			C1,C2,C3,C4,EX,EX5
			trig_coupling: str
			AC,DC,HFREJ,LFREJ
		"""
		# See http://cdn.teledynelecroy.com/files/manuals/automation_command_ref_manual_ws.pdf#page=152
		self.write(f'{trig_source}:TRCP {trig_coupling}')
	@property
	def trigLevel(self):
		return self.query(f'TRIG_LEVEL?')
		
	@trigLevel.setter
	def trigLevel(self, trig_source: str, level: float):
		"""Set the trigger level.
		Parameterers
		------------
		trig_source : str
		C1,C2,C3,C4,EX,EX5
		trig_coupling: float """

		# See https://cdn.teledynelecroy.com/files/manuals/maui-remote-control-and-automation-manual.pdf#page=237
		self.write(f'{trig_source}:TRLV {level}')
	
	@property
	def trigSlope(self):
		# See https://cdn.teledynelecroy.com/files/manuals/maui-remote-control-and-automation-manual.pdf#page=244
		self.query("TRIG_SLOPE?")

	@trigSlope.setter
	def trigSlope(self, trig_source: str, trig_slope: str):
		"""Set the trigger slope.
		Parameterers
		------------
		trig_source : str
		C1,C2,C3,C4,EX,EX5
		trig_slope : str
		Positive, negative.
		"""
		# See https://cdn.teledynelecroy.com/files/manuals/maui-remote-control-and-automation-manual.pdf#page=244
		VALID_TRIG_SLOPES = {'POS', 'NEG'}
		if not isinstance(trig_slope, str) or trig_slope.lower() not in {tslp.lower() for tslp in VALID_TRIG_SLOPES}:
			raise ValueError(f'The trigger coupling must be one of {VALID_TRIG_SLOPES}, received {repr(trig_slope)}...')
		self.write(f'{trig_source}:TRSL {trig_slope}')
	
	def trigDelay(self, trig_delay: float):
		"""Set the trig delay, i.e. the time interval between the trigger event and the center of the screen."""
		# See http://cdn.teledynelecroy.com/files/manuals/tds031000-2000_programming_manual.pdf#page=152
		if not isinstance(trig_delay, (float, int)):
			raise ValueError(f'The trigger delay must be a number, received object of type {type(trig_delay)}.')
		self.write(f'TRIG_DELAY {trig_delay}')
	
	def samplingModeSequence(self, status:str, number_of_segments:int=None)->None:
		"""Configure the "sampling mode sequence" in the oscilloscope. See
		[here](https://cdn.teledynelecroy.com/files/manuals/maui-remote-control-automation_27jul22.pdf#%5B%7B%22num%22%3A1235%2C%22gen%22%3A0%7D%2C%7B%22name%22%3A%22XYZ%22%7D%2C54%2C743.25%2C0%5D).
		
		Arguments
		---------
		status: str
			Either 'on' or 'off'.
		number_of_segments: int
			Number of segments, i.e. number of "sub triggers" within the
			sequence mode.
		"""
		if not isinstance(status, str) or status.lower() not in {'on','off'}:
			raise ValueError(f'`status` must be a string, either "on" or "off", received {status} of type {type(status)}.')
		if number_of_segments is not None and not isinstance(number_of_segments, int):
			raise TypeError(f'`number_of_segments` must be an integer number.')
		cmd = f'SEQUENCE {status.upper()}'
		if number_of_segments is not None:
			cmd += f',{number_of_segments}'
		self.write(cmd)
	
	def sequenceTimeout(self, sequence_timeout:float, enable_sequence_timeout:bool=True):
		"""Configures the "Sequence timeout" in the oscilloscope both value
		and enable/disable.
		
		Arguments
		---------
		sequence_timeout: float
			Timeout value in seconds.
		enable_sequence_timeout: bool, default `True`
			Enable or disable the sequence timeout functionality.
		"""
		if not isinstance(sequence_timeout, (int,float)):
			raise TypeError(f'`sequence_timeout` must be a float number, received object of type {type(sequence_timeout)}.')
		if not enable_sequence_timeout in {True, False}:
			raise TypeError(f'`enable_sequence_timeout` must be a boolean, received object of type {type(enable_sequence_timeout)}.')
		enable_sequence_timeout = 'true' if enable_sequence_timeout==True else 'false'
		self.write(f"VBS 'app.Acquisition.Horizontal.SequenceTimeout = {sequence_timeout}'")
		self.write(f"VBS 'app.Acquisition.Horizontal.SequenceTimeoutEnable = {enable_sequence_timeout}'")


	class Channel:

		def __init__(self, resource, channel:int):
			self._channel= channel
			self._osc=resource

		def get_waveform(self)->dict:
			"""Gets the waveform(s) from the specified channel.
			
			Returns
			-------
			data: dict
				Returns a dictionary of the form
				```
				{
					'waveforms': [{'Time (s)': t, f'Amplitude (V)': s} for t,s in zip(times,samples)],
					'wavedesc': parsed_wavedesc_block,
					'trigtime': parsed_trigtime_block,
				}
				```
				
				The most important field is the `'waveforms'` field, which is
				a list of dictionaries, each of the form
				```
				{
					'Time (s)': numpy.array,
					'Amplitude (V)': numpy.array,
				}
				```
				containing each of the waveforms (many waveforms if TimeBase→Sequence
				is enabled, a single waveform if TimeBase→RealTime is enabled). Note
				that if multiple waveforms are present in the oscilloscope, they
				are split internally such that each element of this list is
				a whole waveform on its own.
				
				The fields `'wavedesc'` and `'trigtime'` contain additional
				information provided by the oscilloscope, for more information
				on these read the text that the oscilloscope provides by
				querying `'TMPL?'`.
			"""
			
			self._osc.write('CORD HI') # High-Byte first
			self._osc.write('COMM_FORMAT DEF9,WORD,BIN') # Communication Format: DEF9 (this is the #9 specification; WORD (reads the samples as 2 Byte integer; BIN (reads in Binary)
			self._osc.write('CHDR OFF')
			self._osc.write(f'C{self._channel}:WF?')
			time.sleep(.1)
			raw_bytes = self._osc.read_raw()
			raw_bytes = raw_bytes[15:] # This I don't understand, the first 15 bytes are some kind of garbage... But this is happening always.
			
			parsed_wavedesc_block = parse_wavedesc_block(raw_bytes)
			samples = parse_data_array_1_block(raw_bytes, parsed_wavedesc_block)
			parsed_trigtime_block = parse_trigtime_block(raw_bytes, parsed_wavedesc_block)
			
			n_samples_per_trigger = int(len(samples)/parsed_wavedesc_block['SUBARRAY_COUNT'])
			samples = [np.array(samples[i*n_samples_per_trigger:(i+1)*n_samples_per_trigger]) for i in range(parsed_wavedesc_block['SUBARRAY_COUNT'])]#np.array(samples).reshape((parsed_wavedesc_block['SUBARRAY_COUNT'],n_samples_per_trigger))
			
			time_array = np.arange(
				start = 0,
				stop = parsed_wavedesc_block['HORIZ_INTERVAL']*(n_samples_per_trigger), 
				step = parsed_wavedesc_block['HORIZ_INTERVAL'],
			)# + parsed_wavedesc_block['HORIZ_OFFSET']
			times = [np.copy(time_array) for i in range(parsed_wavedesc_block['SUBARRAY_COUNT'])]
			
			for i,trigtime in enumerate(parsed_trigtime_block):
				times[i] += trigtime['TRIGGER_OFFSET']
			
			return {
				'wavedesc': parsed_wavedesc_block,
				'trigtime': parsed_trigtime_block,
				'waveforms': [{'Time (s)': t, f'Amplitude ({parsed_wavedesc_block["VERTUNIT"]})': s} for t,s in zip(times,samples)],
			}
			
		def triggerTimes(self)->list:
			"""Gets the trigger times (with respect to the first trigger). What
			this function returns is the list of numbers you find if you go
			in the oscilloscope window to "Timebase→Sequence→Show Sequence Trigger Times...→since Segment 1"
			
			
			Returns
			-------
			trigger_times: list
				A list of trigger times in seconds from the first trigger.
			"""

			raw = self._osc.query(f"VBS? 'return=app.Acquisition.Channels(\"C{self._channel}\").TriggerTimeFromRef'") # To know this command I used the `XStream Browser` app in the oscilloscope's desktop.
			raw = [int(i) for i in raw.split(',') if i != '']
			datetimes = [datetime.datetime.fromtimestamp(i/1e10) for i in raw] # Don't know why we have to divide by 1e10, but it works...
			datetimes = [i-datetimes[0] for i in datetimes]
			return [i.total_seconds() for i in datetimes]
		
		@property
		def vdiv(self):
			"""Gets the vertical scale of the specified channel. Returns a 
			float number with the volts/div value."""

			return float(self._osc.query(f'C{self._channel}:VDIV?')) # http://cdn.teledynelecroy.com/files/manuals/tds031000-2000_programming_manual.pdf#page=47
	
		@vdiv.setter
		def vdiv(self, vdiv: float):
			"""Sets the vertical scale for the specified channel."""
			try:
				vdiv = float(vdiv)
			except:
				raise TypeError(f'<vdiv> must be a float number, received object of type {type(vdiv)}.')

			self._osc.write(f'C{self._channel}:VDIV {float(vdiv)}') # http://cdn.teledynelecroy.com/files/manuals/tds031000-2000_programming_manual.pdf#page=47

		def voffset(self, voffset: float):
			"""Sets the vertical offset for the specified channel."""
			try:
				voffset = float(voffset)
			except:
				raise TypeError(f'<voffset> must be a float number, received object of type {type(voffset)}.')

			self._osc.write(f'C{self._channel}:OFST {float(voffset)}') # http://cdn.teledynelecroy.com/files/manuals/tds031000-2000_programming_manual.pdf#page=43



