PRAGMA foreign_keys = ON;

-----------------------------------------------------------------------------------------
-- tables
-----------------------------------------------------------------------------------------
CREATE TABLE "sitter"
(
       "id" INTEGER PRIMARY KEY  AUTOINCREMENT  NOT NULL ,
       "image" TEXT NOT NULL,
       "name" TEXT NOT NULL ,
       "phone" TEXT NOT NULL,
       "email" TEXT NOT NULL ,
       "ratings_score" REAL,
       "score" REAL,
       "overall_rank" REAL
 );

CREATE TABLE "stay"
(
        "id" INTEGER PRIMARY KEY  AUTOINCREMENT  NOT NULL ,
        "review" TEXT NOT NULL,
        "start_date" TEXT NOT NULL ,
        "end_date" TEXT NOT NULL,
        "rating" REAL NOT NULL,
        "sitter_id" INTEGER,
        "owner_id" INTEGER,
        FOREIGN KEY(sitter_id) REFERENCES sitter(id),
        FOREIGN KEY(owner_id) REFERENCES owner(id)
 );


CREATE TABLE "owner"
(
        "id" INTEGER PRIMARY KEY  AUTOINCREMENT  NOT NULL ,
        "image" TEXT NOT NULL,
        "name" TEXT NOT NULL ,
        "phone_number" TEXT,
        "email" TEXT NOT NULL
);


CREATE TABLE "dog"
(
        "id" INTEGER PRIMARY KEY  AUTOINCREMENT  NOT NULL ,
        "name" TEXT NOT NULL,
        "owner_id", INTEGER,
         FOREIGN KEY(owner_id) REFERENCES owner(id)
);


-----------------------------------------------------------------------------------------
-- views
-----------------------------------------------------------------------------------------
CREATE VIEW "sitterlist" as
SELECT sitter.name AS Sitter,
       sitter.image AS Photo,
       round(sitter.ratings_score,1) AS Rating,
       sitter.overall_rank AS rank
FROM sitter;

-----------------------------------------------------------------------------------------
-- triggers
-----------------------------------------------------------------------------------------

-- search ranking algorithm :  stays * ranking/2 * .1 + score

CREATE TRIGGER update_stay_rating_after_update AFTER
UPDATE OF rating ON stay BEGIN
UPDATE sitter
SET ratings_score =
  (SELECT avg(rating)
   FROM stay
   WHERE sitter_id = new.sitter_id)
WHERE id = new.sitter_id; END;


CREATE TRIGGER update_stay_rating_after_insert AFTER
INSERT ON stay BEGIN
UPDATE sitter
SET ratings_score =
  (SELECT avg(rating)
   FROM stay
   WHERE sitter_id = new.sitter_id)
WHERE id = new.sitter_id; END;

CREATE TRIGGER update_rating_score_after_score_update AFTER
UPDATE OF score ON sitter BEGIN
UPDATE sitter
SET ratings_score =
  (SELECT avg(rating)
   FROM stay
   WHERE sitter_id = new.id)
WHERE id = new.id; END;


CREATE TRIGGER update_rating_score_after_sitter_insert AFTER
INSERT ON sitter BEGIN
UPDATE sitter
SET ratings_score =
  (SELECT avg(rating)
   FROM stay
   WHERE sitter_id = new.id)
WHERE id = new.id; END;


CREATE TRIGGER update_ranking_score_after_ratings_update AFTER
UPDATE OF ratings_score ON sitter BEGIN
UPDATE sitter
SET overall_rank =
  (SELECT CASE
              WHEN
                     (SELECT count(id)
                      FROM stay
                      WHERE sitter_id=new.id) >= 10 THEN ratings_score
              WHEN
                     (SELECT count(id)
                      FROM stay
                      WHERE sitter_id=new.id) = 0 THEN score
              ELSE
                     (SELECT count(id)
                      FROM stay
                      WHERE sitter_id=new.id) * ratings_score/2 * .1 + score
          END
   FROM sitter
   WHERE id=new.id)
WHERE id=new.id;

END;
