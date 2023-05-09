(ns backend.core
  (:require [clojure.string :refer [split]]
            [ring.adapter.jetty :refer [run-jetty]]
            [ring.middleware.reload :refer [wrap-reload]]
            [ring.util.response :refer [bad-request]]
            [clojure.java.io :as io]))

;; List of characters that are reserved in HTTP URIs or Windows or Linux file paths
(def reserved-characters ":/?&=<>\"/\\|*.\0 ")

(def database "database/gardens/")

(defn list-gardens []
  {:status 200
   :headers {"Content-Type" "application/json"}
   :body (->> (io/file database)
              file-seq
              (filter #(.isFile %))
              (map #(.getName %))
              (map #(drop-last 5 %))
              (map #(apply str %))
              (apply vector)
              str)})

(defn get-garden [name]
  {:status 200
   :headers {"Content-Type" "text/plain"}
   :body (slurp (str database name ".json"))})

(defn save-garden [name content]
  (try
    (spit (str database name ".json") content)
    {:status 200}
    (catch Exception _
      {:status 500})))

(defn delete-garden [name]
  {:status 200
   :headers {"Content-Type" "text/plain"}
   :body (str ["delete-garden" name])})

(defn rename-garden [old-name new-name]
  {:status 200
   :headers {"Content-Type" "text/plain"}
   :body (str ["rename-garden" old-name new-name])})

(defn handler [request]
  (let [segments (filter not-empty (split (:uri request) #"/"))]
    (cond
      (= segments ["inspect"]) (bad-request (str request))
      (= segments ["gardens" "list"]) (list-gardens)
      (and (= (take 2 segments) ["gardens" "get"])
           (= (count segments) 3)) (get-garden (last segments))
      (and (= (take 2 segments) ["gardens" "save"])
           (= (count segments) 3)) (save-garden (last segments) (:body request))
      (and (= (take 2 segments) ["gardens" "delete"])
           (= (count segments) 3)) (delete-garden (last segments))
      (and (= (take 2 segments) ["gardens" "rename"])
           (= (count segments) 4)) (let [arguments (drop 2 segments)]
                                     (rename-garden (first arguments)
                                                    (second arguments)))
      :else (bad-request (str "not-found: " (apply vector segments))))))

(def app
  (wrap-reload #'handler))

(defn -main []
  (run-jetty app {:port 3000}))
