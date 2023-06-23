CREATE OR REPLACE FUNCTION 
improveSomeRatingsFunction(theParty TEXT, maxRatingImprovements INTEGER)
RETURNS INTEGER AS $$

DECLARE
    ratingImprovements INTEGER := 0;

BEGIN
    UPDATE OfficeHolders AS oh
    SET rating = CASE WHEN oh.rating = 'B' THEN 'A'
                     WHEN oh.rating = 'C' THEN 'B'
                     WHEN oh.rating = 'D' THEN 'C'
                     WHEN oh.rating = 'F' THEN 'D'
                     ELSE oh.rating
    END

    FROM CandidatesForOffice AS cfo
    WHERE cfo.candidateID = oh.candidateID
        AND cfo.officeID = oh.officeID
        AND cfo.electionDate = oh.electionDate
        AND cfo.party = theParty
        AND oh.rating IN ('B', 'C', 'D', 'F')
        AND ratingImprovements < maxRatingImprovements;

    GET DIAGNOSTICS ratingImprovements = ROW_COUNT;

    RETURN ratingImprovements;
END;
$$ LANGUAGE plpgsql;