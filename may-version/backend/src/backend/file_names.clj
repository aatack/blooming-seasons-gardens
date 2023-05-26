(ns backend.file-names
  (:require [clojure.string :refer [escape replace]]))

;; List of characters that are reserved in HTTP URIs or Windows or Linux file paths.
;; The ordering is important here because braces are used for the escaping of file
;; names, and so need to be processed last
(def character-to-escape-sequence-array
  [[":" "colon"]
   ["?" "question"]
   ["&" "and"]
   ["=" "equal"]
   ["<" "open-bracket"]
   [">" "close-bracket"]
   ["\"" "quote"]
   ["/" "slash"]
   ["\\" "backslash"]
   ["|" "pipe"]
   ["*" "star"]
   ["." "dot"]
   [" " "space"]
   ["~" "tilde"]
   ["{" "open-brace"]
   ["}" "close-brace"]])

(def character-to-escape-sequence-map
  (->> character-to-escape-sequence-array
       (map (fn [[character escape-sequence]]
              [(first character) escape-sequence]))
       (into {})))

(defn escape-file-name [file-name]
  (escape file-name #(when (character-to-escape-sequence-map %)
                       (str "{" (character-to-escape-sequence-map %) "}"))))

(defn unescape-file-name [file-name]
  (reduce (fn [unescaped [match replacement]]
            (replace unescaped (re-pattern (str "\\{" replacement "\\}")) match))
          file-name
          character-to-escape-sequence-array))
