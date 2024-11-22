(ns backend.core
  (:require [backend.file-names :refer [escape-file-name unescape-file-name]]
            [cheshire.core :refer [generate-string parse-string]]
            [clojure.java.io :as io]
            [ring.adapter.jetty :refer [run-jetty]]
            [ring.middleware.cors :refer [wrap-cors]]
            [ring.middleware.reload :refer [wrap-reload]]
            [ring.util.request :refer [body-string]]))

(def database "database/gardens/")

(defn list-gardens []
  (->> (io/file database)
       file-seq
       (filter #(.isFile %))
       (map #(.getName %))
       (map #(drop-last 5 %))
       (map #(apply str %))
       (map unescape-file-name)
       (apply vector)))

(defn get-garden [name]
  (parse-string (slurp (str database (escape-file-name name) ".json"))))

(defn save-garden [name content]
  (spit (str database (escape-file-name name) ".json") (generate-string content)))

(defn delete-garden [name]
  (io/delete-file (str database (escape-file-name name) ".json")))

(defn rename-garden [old-name new-name]
  (.renameTo (io/file (str database (escape-file-name old-name) ".json"))
             (io/file (str database (escape-file-name new-name) ".json"))))

(defn handle-clojure [uri body]
  (case uri
    "/body" (str body)
    "/garden/list" (list-gardens)
    "/garden/get" (get-garden (body "name"))
    "/garden/save" (save-garden (body "name") (body "content"))
    "/garden/delete" (delete-garden (body "name"))
    "/garden/rename" (rename-garden (body "old-name") (body "new-name"))))

(defn routes [request]
  (let [uri (:uri request)
        body (parse-string (body-string request))]
    (try (let [response (generate-string (handle-clojure uri body))]
           {:status 200
            :headers {"Content-Type" "application/json"}
            :body (if (string? response) response (generate-string response))})
         (catch Exception error
           {:status 500
            :headers {"Content-Type" "text/plain"}
            :body (str error)}))))

(def handler (->
              (wrap-reload #'routes)
              (wrap-cors :access-control-allow-origin #".*"
                         :access-control-allow-methods [:get :put :post :delete])))

(defn -main []
  (run-jetty handler {:port 3000}))
