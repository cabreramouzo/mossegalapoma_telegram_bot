from main import split_user_message_info, add_username_to_proposal_reply, add_username_to_proposal_reply, generate_random_index_for_reply, generate_random_response_for
from replies import text_reply_proposal, text_reply_errata, text_reply_palasaca, text_rich_reply_proposal_disney_plus, text_rich_reply_proposal_hbo, text_rich_reply_proposal_netflix, text_troll_reply
from emoji_unicode import *

def test_split_user_info():

	class Telegram_user:

		def __init__(self, username: str, first_name: str, last_name:str):

			self.username = username
			self.first_name = first_name
			self.last_name = last_name

	class Effective_message:

		def __init__(self, text: str, from_user: Telegram_user):

			self.text = text
			self.from_user = from_user

	class Update:

		def __init__(self, effective_message: Effective_message):

			self.effective_message = effective_message


	fake_telegram_user = Telegram_user("macma", "Miguel Ángel", "Cabrera Mouzo")
	fake_effective_message = Effective_message("Tinc una nova #propostamossegui nois!", fake_telegram_user)
	fake_update = Update(fake_effective_message)

	user_name, user_first_name, user_last_name, user_text = split_user_message_info(fake_update)

	assert user_name == "macma"
	assert user_first_name == "Miguel Ángel"
	assert user_last_name == "Cabrera Mouzo"
	assert user_text == "Tinc una nova #propostamossegui nois!"

def test_add_username_to_proposal_reply():
	user_name = 'macma'
	len_old =  len( text_reply_proposal )
	replies = add_username_to_proposal_reply('macma', text_reply_proposal)
	expected = [
		f"Saps @{user_name}, jo també ho anava a proposar... {grinning_face_smiling_eyes}",
		f"A veure, @{user_name}. Aquesta és bona {winking_face}",
		f"@{user_name}, seguim endavant gràcies a tu {face_blowing_a_kiss}",
		f"@{user_name}, sense tu això no seria possible {face_blowing_a_kiss}",
		f"@{user_name}, necessitem mosseguis com tu per tirar això endavant. Merci! {grinning_face_smiling_eyes}",
		f"Quan tinguem el Tesla, @{user_name} seràs dels primers a provar-lo! {sun_glasses} Paraula de Bot {robot}",
		f"@{user_name}, saps que en @tomasmanz t'estima molt, oi? Jo en canvi... és complicat. {robot}"

	]

	assert len(replies) == len_old + len(expected)
	for phrase in expected:
		assert phrase in replies
	
def xtest_look_for_hashtags():
	pass

def test_generate_random_int_reply():

	types = ['proposta','errata','disney_plus','netflix','hbo','troll','palasaca']

	def get_type_len(type_):
		if type_ == 'proposta':
			return len(text_reply_proposal)
		elif type_ == 'errata':
			return len(text_troll_reply)
		elif type_ == 'disney_plus':
			return len(text_rich_reply_proposal_disney_plus)
		elif type_ == 'netflix':
			return len(text_rich_reply_proposal_netflix)
		elif type_ == 'hbo':
			return len(text_rich_reply_proposal_hbo)
		elif type_ == 'troll':
			return len(text_troll_reply)
		elif type_ == 'palasaca':
			return len(text_reply_palasaca)
		

	for type_ in types:
		randint = generate_random_index_for_reply(type_)
		assert randint >= 0 and randint <= get_type_len(type_)

		
def test_generate_random_reply_for_type():

	types = ['proposta','errata','disney_plus','netflix','hbo','troll','palasaca']

	def get_reply_list(type_):
		if type_ == 'proposta':
			return text_reply_proposal
		elif type_ == 'errata':
			return text_reply_errata
		elif type_ == 'disney_plus':
			return text_rich_reply_proposal_disney_plus
		elif type_ == 'netflix':
			return text_rich_reply_proposal_netflix
		elif type_ == 'hbo':
			return text_rich_reply_proposal_hbo
		elif type_ == 'troll':
			return text_troll_reply
		elif type_ == 'palasaca':
			return text_reply_palasaca
		

	for type_ in types:
		response = generate_random_response_for(type_)
		assert response in get_reply_list(type_)

			
