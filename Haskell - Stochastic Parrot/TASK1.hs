import Data.Char
import Data.Maybe
import Data.List 
import System.Random

main = do
      book <- readFile "BOOKS/pg25420.txt"
      let n = 2
          words = preProcess (lower book)
          ngrams = generateNGrams n words
          seed = genRandomSeed ngrams (genRandomInd n words)
          output = generateText 30 seed ngrams
      print (unwords output)

--lower all word in book
lower xs = map toLower xs

--checks for space in string (normal isSpace allowed control characters) 
isSpaceLocal x 
    | x == ' ' = True
    | otherwise =  False 

--preprocess book 
preProcess =  words . filter (\x -> isAlphaNum x || isSpaceLocal x)

--gets the next element in the list
nextElemList _ [] = []
nextElemList x xs
        | length xs < 3 = []
        | n == Nothing = []
        | length x > 1 && (xs!!(ind+1) == x!!1)  = xs!!(ind+2) : nextElemList x (tail (dropWhile (/=(x!!0)) xs))
        | length x == 1 = xs!!(ind+1) : nextElemList x (tail (dropWhile (/=x!!0) xs)) 
        | otherwise = []
    where 
      n = elemIndex (x!!0) xs
      ind = fromJust n

--generates ngrams
generateNGrams n xs 
    | length xs < n = []
    | otherwise = (gram,nextElemList gram xs) : generateNGrams n (tail xs)
    where
        ind = fromJust (elemIndex x xs)
        gram | n > 1 = [xs!!ind,xs!!(ind+1)]
             | n == 1 = [x]

        x = head xs

--generate a random index from a range
genRandomInd n words = max 0 (fst (randomR (0, ((length words)-1)) (mkStdGen n)))

--select a random word using a random index to be used as a seed
genRandomSeed [] _ = []
genRandomSeed words ind = fst (words!!ind)

--select a random word using a random index
randomSelect _ _ [] = []
randomSelect word n ((key,values):xs)
    | word == key && length word > 1 && length values>=idx = [word!!1,values!!idx]
    | word == key && length values>=idx = [values!!idx]
    | otherwise = randomSelect word n xs
    where
      idx = (genRandomInd n values) 



generateText :: Int -> [String] -> [([String],[String])] -> [String]
generateText 0 [] _ = []
generateText 0 seed _ = tail seed
generateText m seed ngrams
    | x == [] = (". " ++ (unwords newSeed)) : generateText (m-1) newSeed ngrams
    | otherwise = x!!0 : generateText (m-1) x ngrams
    where 
      x = randomSelect seed m ngrams
      newSeed = genRandomSeed ngrams (genRandomInd m ngrams)