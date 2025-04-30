import Data.Char
import Data.List
import System.Random
import qualified Data.Map as Map

main = do
    book <- readFile "BOOKS/pg25420.txt"
    let n = 3  -- Set n to any desired n-gram size
        words = preProcess (lower book)
        ngrams = generateNGrams n words
        seed = genRandomSeed ngrams
        output = generateText 30 seed ngrams
    putStrLn (unwords output)

-- Convert all characters to lowercase
lower :: String -> String
lower = map toLower

-- Check for space or alphanumeric character
isSpaceLocal :: Char -> Bool
isSpaceLocal x = isAlphaNum x || x == ' '

-- Preprocess the text by filtering only alphanumeric and space characters
preProcess :: String -> [String]
preProcess = words . filter isSpaceLocal

-- Generate n-grams of any length n using a sliding window
generateNGrams :: Int -> [String] -> Map.Map [String] [String]
generateNGrams n xs
    | length xs < n = Map.empty
    | otherwise = Map.fromListWith (++) (ngrams xs)
  where
    ngrams ys
        | length ys < n = []
        | otherwise = (prefix, [ys !! n]) : ngrams (tail ys)
        where prefix = take n ys

-- Generate a random seed word sequence from n-grams keys
genRandomSeed :: Map.Map [String] [String] -> [String]
genRandomSeed ngrams = fst $ Map.elemAt (fst (randomR (0, Map.size ngrams - 1) (mkStdGen 42))) ngrams

-- Select the next word based on the current seed from the n-grams
randomSelect :: RandomGen g => g -> [String] -> Map.Map [String] [String] -> ([String], g)
randomSelect gen key ngrams = case Map.lookup key ngrams of
    Just values ->
        let (idx, newGen) = randomR (0, length values - 1) gen
        in (key ++ [values !! idx], newGen)
    Nothing -> ([], gen)

-- Generate text of a given length
generateText :: Int -> [String] -> Map.Map [String] [String] -> [String]
generateText 0 seed _ = seed
generateText m seed ngrams
    | null next = seed
    | otherwise = generateText (m - 1) next ngrams
  where
    (_, gen) = randomR (0, 1) (mkStdGen m)
    (next, _) = randomSelect gen seed ngrams
