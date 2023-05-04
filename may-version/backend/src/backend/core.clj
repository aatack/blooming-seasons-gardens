(ns backend.core
  (:require [clojure.string :refer [split]]
            [ring.adapter.jetty :refer [run-jetty]]
            [ring.middleware.reload :refer [wrap-reload]]
            [ring.util.response :refer [response]]))

(defn handler [request]
  (let [segments (filter not-empty (split (:uri request) #"/"))]
    (response
     (cond
       (= segments ["inspect"]) (str request)
       (= segments ["gardens"]) "gardens"
       :else (str "not known" segments request)))))

(def app
  (wrap-reload #'handler))

(defn -main []
  (run-jetty app {:port 3000}))
