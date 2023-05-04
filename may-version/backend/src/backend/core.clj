(ns backend.core
  (:require [clojure.string :refer [split]]
            [ring.adapter.jetty :refer [run-jetty]]
            [ring.middleware.reload :refer [wrap-reload]]
            [ring.util.response :refer [status content-type bad-request]]))

(defn list-gardens []
  {:status 200
   :headers {"Content-Type" "text/plain"}
   :body "list-gardens"})

(defn get-garden [name]
  {:status 200
   :headers {"Content-Type" "text/plain"}
   :body (str ["get-garden" name])})

(defn put-garden [name content]
  {:status 200
   :headers {"Content-Type" "text/plain"}
   :body (str ["put-garden" name content])})

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
      (and (= segments ["garden"])
           (= (:request-method request) :get)
           (= (count segments) 1)) (list-gardens)
      (and (= (first segments) "garden")
           (= (:request-method request) :get)
           (= (count segments) 2)) (get-garden (second segments))
      :else (bad-request (apply str "not-found: " segments)))))

(def app
  (wrap-reload #'handler))

(defn -main []
  (run-jetty app {:port 3000}))
