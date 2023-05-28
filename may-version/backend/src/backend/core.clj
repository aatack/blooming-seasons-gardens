(ns backend.core
  (:require [backend.file-names :refer [escape-file-name unescape-file-name]]
            [cheshire.core :refer [generate-string]]
            [clojure.java.io :as io]
            [clojure.string :refer [split]]
            [ring.adapter.jetty :refer [run-jetty]]
            [ring.middleware.cors :refer [wrap-cors]]
            [ring.middleware.reload :refer [wrap-reload]]
            [ring.util.response :refer [bad-request]]))

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
              (map unescape-file-name)
              (apply vector)
              generate-string)})

(defn get-garden [name]
  {:status 200
   :headers {"Content-Type" "text/plain"}
   :body (slurp (str database (escape-file-name name) ".json"))})

(defn save-garden [name content]
  (try
    (spit (str database (escape-file-name name) ".json") content)
    {:status 200}
    (catch Exception _
      {:status 500})))

(defn delete-garden [name]
  (io/delete-file (str database (escape-file-name name) ".json"))
  {:status 200
   :headers {"Content-Type" "text/plain"}
   :body (str "Deleted " name)})

(defn rename-garden [old-name new-name]
  (let [success (.renameTo (io/file (str database old-name ".json"))
                           (io/file (str database new-name ".json")))]
    (if success
      {:status 200
       :headers {"Content-Type" "text/plain"}
       :body (str "Renamed " old-name " to " new-name)}
      (bad-request (str "Could not rename " old-name " to " new-name)))))

(defn routes [request]
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

(def handler (->
              (wrap-reload #'routes)
              (wrap-cors :access-control-allow-origin #".*"
                         :access-control-allow-methods [:get :put :post :delete])))

(defn -main []
  (run-jetty handler {:port 3000}))
