import pandas as pd 

df = pd.read_csv('/home/mil/k-tanaka/new_meme_dataset_2/new_meme_dataset_2/scraping/csv_files/scraped_memes.csv')

replace_dict = {
    "Goodfellas-Laugh.jpg" : "Wise-guys-laughing.jpg",
    'Good-Fellas-Hilarious.jpg' : "Wise-guys-laughing.jpg",
    'Sidious-Error.jpg' : "Emperor-Palpatine.jpg",
    'That-Would-Be-Great.jpg' : "Yeah-if-you-could.jpg",
    'Lumbergh.jpg' : "Yeah-if-you-could.jpg",
    'Old-lady-at-computer-finds-the-Internet.jpg' : "Grandma-Finds-The-Internet.jpg",
    'Star-Trek-Kirk-Khan.jpg' : "Captain-Kirk-Khan.jpg",
    'khan.jpg' : "Captain-Kirk-Khan.jpg",
    'stoned-guy.jpg' : "10-Guy.jpg",
    'HighDrunk-guy.jpg' : "10-Guy.jpg",
    'We-Want-you.jpg' : "I-WANT-YOU.jpg",
    'Please-sir-may-I-have-some-more.jpg' : "Oliver-Twist-Please-Sir.jpg",
    'Picard-Wtf.jpg' : "startrek.jpg",
    'Not-sure-if--fry.jpg' : "Futurama-Fry.jpg",
    'crack.jpg' : "Crack-head.jpg",
    'Mugatu-So-Hot-Right-Now.jpg' : "So-Hot-Right-Now.jpg",
    'Ancient-Aliens.jpg' : "Aliens-Guy.jpg",
    'Dinosaur.jpg' : "Philosoraptor.jpg",
    'Do-you-want-ants-archer.jpg' : "Archer.jpg",
    'Dr-Evil-Quotes.jpg' : "Dr-Evil-air-quotes.jpg",
    'Smart-black-guy.jpg' : "Black-guy-head-tap.jpg",
    'Smart-Guy.jpg' : "Black-guy-head-tap.jpg",
    'Why-you-no.jpg' : "Y-U-No.jpg",
    'Pepe-Silvia.jpg' : "Charlie-Day.jpg",
    'conspiracy-theory.jpg' : "Charlie-Day.jpg",
    'Trying-to-explain.jpg' : "Charlie-Day.jpg",
    'Thats-my-secret.jpg' : "Hulk.jpg",
    'Chubby-Bubbles-Girl.jpg' : "girl-running.jpg",
    'The-future-world-if.jpg' : "society-if.jpg",
    'computer-nerd.jpg' : "Internet-Guide.jpg",
    'Skeleton-Computer.jpg' : "Waiting-Skeleton.jpg",
    'Laughing-Men-In-Suits.jpg' : "And-Then-He-Said.jpg",
    'Rich-men-laughing.jpg' : "And-Then-He-Said.jpg",
    'michael-jackson-eating-popcorn.jpg' : "Michael-Jackson-Popcorn.jpg",
    'Black-Scientist-Finally-Xium.jpg' : "FINALLY.png",
    'You-keep-using-that-word.jpg' : "Inigo-Montoya.jpg",
    'Black-guy-hiding-behind-tree.png' : "Licking-lips.png",
    'Sean-Bean-Lord-Of-The-Rings.jpg' : "Walk-Into-Mordor.jpg",
    "Cat-newspaper.jpg" : 'I-Should-Buy-A-Boat-Cat.jpg'
}

df = df.replace({'filename' : replace_dict})

df.to_csv('/home/mil/k-tanaka/new_meme_dataset_2/new_meme_dataset_2/scraping/csv_files/edited_scraped_memes.csv', index=False)